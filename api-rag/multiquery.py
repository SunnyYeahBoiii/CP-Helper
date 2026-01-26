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
def generate_queries_alternative(question: str):
    """Generate multiple query perspectives using remote API"""
    import httpx
    import json
    
    template = """Generate exactly 5 different versions of this question for better document retrieval.
Return ONLY the questions, one per line. No explanations, no numbers, no conversational text.

Original question: {question}

Alternative questions:"""
    
    full_prompt = template.format(question=question)
    
    payload = {
        "model": "llama3:latest",
        "messages": [
            {
                "role": "user",
                "content": full_prompt
            }
        ]
    }

    print(f"Query generation prompt: {full_prompt}")
    
    try:
        with httpx.Client() as client:
            response = client.post(
                "https://1f2344524333.ngrok-free.app/api/chat",
                json=payload,
                timeout=30.0
            )
            response.raise_for_status()
            
            full_content = ""
            response_text = response.text
            print(f"Raw response: {response_text}")
            
            # Parse streaming JSON response
            for line in response_text.split('\n'):
                line = line.strip()
                if line:
                    try:
                        parsed = json.loads(line)
                        if parsed.get("message", {}).get("content"):
                            content = parsed["message"]["content"]
                            full_content += content
                    except json.JSONDecodeError:
                        continue
            
            print(f"Parsed content: {full_content}")
            
            # Better query filtering
            queries = []
            for line in full_content.split("\n"):
                line = line.strip()
                # Filter out non-questions and conversational text
                if (line and 
                    not line.lower().startswith(('here are', 'these alternative', 'original question:', 'questions:', 'alternative')) and
                    '?' in line and  # Must be a question
                    len(line) > 10 and  # Must be substantial
                    not line.isnumeric()):
                    queries.append(line)
            
            # Ensure we have some queries, or use fallback
            if len(queries) < 3:
                print(f"Only got {len(queries)} valid queries, using original question")
                return [question]
            
            print(f"Generated queries: {queries[:5]}")
            return queries[:5]  # Return exactly 5
            
    except Exception as e:
        print(f"Error generating queries: {e}")
        # Fallback to original question if API fails
        return [question]

generate_queries = generate_queries_alternative

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
    """Retrieve documents with better error handling"""
    try:
        print("Generating queries...")
        docs = generate_queries(question)
        print(f"Generated {len(docs)} queries: {docs}")
        
        if not docs:
            print("No queries generated, using original question")
            docs = [question]
        
        print("Retrieving documents...")
        result = [retriever.invoke(doc) for doc in docs]
        print(f"Retrieval results: {[len(docs_list) for docs_list in result]}")
        
        final_docs = get_unique_union(result)
        print(f"Final unique documents: {len(final_docs)}")
        return final_docs
        
    except Exception as e:
        print(f"Error in retrieve_documents: {e}")
        # Fallback: try direct retrieval with original question
        try:
            return retriever.invoke(question)
        except Exception as fallback_error:
            print(f"Fallback also failed: {fallback_error}")
            return []

def query(question: str, stream: bool = False):
    """
    Retrieve context for the question and return the full prompt
    """
    context = ""

    print("=== QUERY FUNCTION START ===")
    print(f"Question: {question}")
    
    docs = retrieve_documents(question)
    print(f"Retrieved {len(docs)} documents")
    
    if not docs:
        print("No documents found, returning empty context")
        context = "No relevant information found in the database."
    else:
        for match in docs:
            title = match.metadata['title']
            pre = match.metadata['prechunk']
            content = match.page_content
            post = match.metadata['postchunk']
            
            print(f"Processing document: {title}")
            context += '\n--------\nTitle: '
            context += title
            context += '\n'
            context += pre
            context += '\n'
            context += content
            context += '\n'
            context += post
            context += '\n'

    print(f"Built context length: {len(context)}")
    
    full_prompt = f'''
    You are a extremely helpful assistant in Competitive Programming. 
    Use the info in the context to answer the question as much detailed as possible. 
    If the question have no relation to the context provided, just answer like usual.
    If there are any code, implement it fully and dont hide any line.

    If you cannot answer, just say "I don't know"

    Context:
    {context}

    Question:
    {question}
    '''

    print(f"Generated prompt length: {len(full_prompt)}")
    
    return full_prompt