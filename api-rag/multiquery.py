from semantic_router.splitters import RollingWindowSplitter
from semantic_router.utils.logger import logger
from semantic_router.encoders import HuggingFaceEncoder
import numpy as np
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
import os

from unstructured.partition.md import partition_md

load_dotenv()

def process_mdx_advanced(file_path):
    # partition_md tự động xử lý frontmatter và cấu trúc markdown
    elements = partition_md(filename=file_path)
    
    # Gộp các element lại thành văn bản
    full_text = "\n\n".join([str(el) for el in elements])
    return full_text


from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.vectorstores import Pinecone
from langchain_ollama import ChatOllama
from langchain_pinecone import PineconeVectorStore
from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="nomic-ai/nomic-embed-text-v1.5",
    model_kwargs={'trust_remote_code': True},
    encode_kwargs={
        'normalize_embeddings': True,  # Semantic Router does this by default
    }
)
vector_store = PineconeVectorStore(
    pinecone_api_key=os.getenv("PINECONE_API_KEY"),
    embedding=embeddings,
    index_name='cp-rag',
    text_key="content"
)

retriever = vector_store.as_retriever(kwargs={"k": 5})

template="""You are an AI language model assistant. Your task is to generate five 
different versions of the given user question to retrieve relevant documents from a vector 
database. By generating multiple perspectives on the user question, your goal is to help
the user overcome some of the limitations of the distance-based similarity search. 
Provide these alternative questions separated by newlines. Original question: {question}"""
prompt_perspectives = ChatPromptTemplate.from_template(template)
generate_queries = (
    prompt_perspectives 
    | ChatOllama(model="llama3")  # Use smaller 8B parameter model
    | StrOutputParser() 
    | (lambda x: [
        line.strip()                            # Remove whitespace
        for line in x.split("\n") 
        if line.strip() and not line.strip().isnumeric() # Remove empty lines and stray numbers
      ])
)

def get_unique_union(documents: list[list]):
    """ Flattens a list of lists of documents and removes duplicates. """
    flattened = [doc for sublist in documents for doc in sublist]
    unique_docs = {}
    for doc in flattened:
        # Use page_content as the unique key
        if doc.page_content not in unique_docs:
            unique_docs[doc.page_content] = doc
    return list(unique_docs.values())

def retrieve_documents(question: str):
    # generate_queries returns List[str]
    # retriever.map() expects List[str] and returns List[List[Document]]
    # get_unique_union expects List[List[Document]] and returns List[Document]
    print("enter")
    retrieval_chain = generate_queries
    docs = retrieval_chain.invoke({"question": question})
    print(docs)
    result = [retriever.invoke(doc) for doc in docs]
    return get_unique_union(result)

def query(question: str, stream: bool = False):
    context = ""

    print("start")
    docs = retrieve_documents(question)
    for match in docs:
        title = match.metadata['title']
        pre = match.metadata['prechunk']
        content = match.page_content
        post = match.metadata['postchunk']

        context += '\n--------\nTitle: '
        context += title
        context += '\n'
        context += pre
        context += '\n'
        context += content
        context += '\n'
        context += post
        context += '\n'

    full_prompt = f'''
    You are a extremely helpful assistant in Competittive Programming. 
    Use the info in the context to answer the question as much detailed as possible. 
    If there are any code, implement it fully and dont hide any line.

    If you cannot answer, just say "I don't know"

    Context:
    {context}

    Question:
    {question}
    '''

    import ollama

    try:
        response = ollama.chat(
            model='llama3',
            messages=[{'role': 'user', 'content': full_prompt}],
            stream=True
        )
        
        if stream:
            # Return generator for streaming
            for chunk in response:
                content = chunk['message']['content']
                print(content, end='', flush=True)
                yield content
            print()
        else:
            # Return full content for non-streaming
            full_content = ""
            for chunk in response:
                content = chunk['message']['content']
                print(content, end='', flush=True)
                full_content += content
            print()
            return full_content
        
    except Exception as e:
        print(f"Lỗi khi gọi model: {e}")
        if stream:
            yield f"Error: {str(e)}"
        else:
            return f"Error: {str(e)}"