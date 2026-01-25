# CP-Helper RAG Core

> **RAG Engine** (Retrieval-Augmented Generation) chuyên dụng cho Competitive Programming, sử dụng Local LLM (Llama3) và Semantic Chunking để tra cứu tài liệu VNOI/USACO chính xác.

Dự án này là phần lõi xử lý AI (Backend/Worker), hoạt động độc lập để cung cấp khả năng trả lời câu hỏi học thuật dựa trên dữ liệu thật.

## Tech Stack

*   **LLM:** [Meta Llama 3](https://ollama.com/library/llama3) (chạy local qua **Ollama**)
*   **Vector Database:** [Pinecone](https://www.pinecone.io/) (Serverless Index)
*   **Embeddings:** `nomic-ai/nomic-embed-text-v1.5` (Matryoshka Embeddings, 768 dim)
*   **Chunking Strategy:** [Semantic Router](https://github.com/aurelio-labs/semantic-router) (Context-aware splitting)
*   **Framework:** Python 3.10+, LangChain

## Tính năng nổi bật

*   **Semantic Chunking:** Thay vì cắt văn bản theo số ký tự cố định, hệ thống sử dụng `Semantic Router` để cắt tài liệu theo ý nghĩa và ngữ cảnh, giúp LLM hiểu trọn vẹn một định lý hoặc thuật toán.
*   **High Quality Embeddings:** Sử dụng `nomic-embed-text-v1.5` với tiền tố `search_query` / `search_document` để tối ưu hóa kết quả tìm kiếm vector.
*   **Local Privacy:** Toàn bộ quá trình sinh câu trả lời (Generation) chạy local trên máy của bạn với Llama3, không tốn phí API OpenAI.

## Cấu trúc dự án

```bash
CP-RAG
├── data/                   
├── src/
│   ├── ingestion.py        
│   ├── rag_chain.py        
│   └── utils.py            
├── .env.example            
├── main.py                 
└── requirements.txt        
