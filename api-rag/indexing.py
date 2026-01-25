from semantic_router.splitters import RollingWindowSplitter
from semantic_router.utils.logger import logger
from semantic_router.encoders import HuggingFaceEncoder
import numpy as np
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
import os

from unstructured.partition.md import partition_md

def process_mdx_advanced(file_path):
    # partition_md tự động xử lý frontmatter và cấu trúc markdown
    elements = partition_md(filename=file_path)
    
    # Gộp các element lại thành văn bản
    full_text = "\n\n".join([str(el) for el in elements])
    return full_text

load_dotenv()

encoder = HuggingFaceEncoder(name="nomic-ai/nomic-embed-text-v1.5", score_threshold=0.5 , trust_remote_code=True)

logger.setLevel("WARNING")

splitter = RollingWindowSplitter(
    encoder=encoder,
    min_split_tokens=50,
    max_split_tokens=20000,
    window_size=2,
    plot_splits=True,
    enable_statistics=True
)

pinecone_api = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key=pinecone_api)

spec = ServerlessSpec(
    cloud='aws',  # or 'gcp', 'azure'
    region='us-east-1'  # choose appropriate region
)

# Create index if not exists
index_name = 'cp-rag'
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=768,  # Match your encoder's output dim (e.g., BGE-M3 is 1024? Wait, check encoder)
        metric='cosine',
        spec=spec
    )

# Connect to index
index = pc.Index(index_name)

def build_chunk(title: str , content: str):
        return f"# {title} \n{content}"

def insert_embeddings(title:str , file_path: str):
    text = process_mdx_advanced(file_path=file_path)

    splits = splitter([text])

    metadata = []
    for i, s in enumerate(splits):
        pre_chunk = "" if i == 0 else splits[i - 1].content
        post_chunk = "" if i + 1 == len(splits) else splits[i + 1].content

        metadata.append({
            "title": title,
            "content": s.content,
            "prechunk": pre_chunk,
            "postchunk": post_chunk,
        })

    vectors = []
    for i, meta in enumerate(metadata):
        # Embed the content
        embedding = encoder([meta['content']])[0]  # or use splitter/encoder as needed
        vectors.append({
            'id': f'${title}-{i}',
            'values': embedding,  # Convert to list
            'metadata': {
                'title': meta['title'],
                'content': meta['content'],
                'prechunk': meta['prechunk'],
                'postchunk': meta['postchunk']
            }
        })

    print(vectors)
    # Upsert in batches
    batch_size = 100
    for i in range(0, len(vectors), batch_size):
        batch = vectors[i:i+batch_size]
        index.upsert(vectors=batch)
    
import glob
import re
from tqdm import tqdm 

def process_all_documents(input_folder, output_folder=None):
    # Tạo đường dẫn tìm kiếm: ./documents/*.mdx
    # recursive=True giúp tìm cả trong các thư mục con (nếu có)
    search_path = os.path.join(input_folder, "**", "*.mdx")
    
    # Lấy danh sách tất cả file mdx
    files = glob.glob(search_path, recursive=True)
    
    print(f"🔍 Tìm thấy {len(files)} file .mdx trong '{input_folder}'")
    
    results = []
    
    # Dùng tqdm để hiện thanh loading bar khi chạy
    for file_path in tqdm(files, desc="Đang xử lý"):
        print(file_path)
        try:
            title = file_path[12:]
            title = title[:-4]
            
            insert_embeddings(title=title , file_path=file_path)
            
        except Exception as e:
            print(f"❌ Lỗi khi đọc file {file_path}: {e}")
            
    return results

def file_listing():
    INPUT_DIR = "./documents"
    OUTPUT_DIR = "./processed_txt" # Nơi lưu file txt kết quả (nếu cần)
    
    # Cài đặt tqdm nếu chưa có: pip install tqdm
    if not os.path.exists(INPUT_DIR):
        print(f"⚠️ Thư mục '{INPUT_DIR}' không tồn tại!")
        # Tạo thư mục mẫu để test
        os.makedirs(INPUT_DIR)
        print(f"✅ Đã tạo thư mục mẫu '{INPUT_DIR}'. Hãy copy file .mdx vào đó.")
    else:
        # Gọi hàm xử lý
        processed_data = process_all_documents(INPUT_DIR, OUTPUT_DIR)
        
        print(f"\n✅ Hoàn tất! Đã xử lý {len(processed_data)} file.")
        
        # Ví dụ: In thử nội dung file đầu tiên

file_listing()