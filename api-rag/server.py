from multiquery import query

# server.py
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import ollama
import json
import httpx
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration from environment variables
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000").split(",")
LLM_API_URL = os.getenv("LLM_API_URL", "http://localhost:11434/api/chat")



# --- 1. SETUP RAG (Copy phần khởi tạo từ code cũ của bạn vào đây) ---
# Ví dụ giả định bạn đã có biến 'index' (Pinecone) và 'encoder' sẵn sàng
# from my_rag_module import index, encoder 
# (Hoặc paste code khởi tạo index/encoder vào đây)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

# Định nghĩa cấu trúc dữ liệu đầu vào
class QueryRequest(BaseModel):
    question: str

# --- 3. ĐỊNH NGHĨA API ENDPOINT ---
@app.options("/api/chat")
async def chat_options():
    return {"status": "ok"}

@app.post("/api/chat")
async def chat_endpoint(request: QueryRequest):
    """
    API nhận câu hỏi -> Chạy RAG -> Gửi đến reasoning API -> Trả về câu trả lời streaming
    """
    print("QUESTION " , request.question)
    
    async def generate_stream():
        try:
            # 1. Get RAG context (non-streaming for now)
            rag_response_generator = query(request.question, stream=False)
            rag_response = ""
            chunk_count = 0
            for chunk in rag_response_generator:
                rag_response += chunk
                chunk_count += 1
            
            print(f"RAG Response received: {chunk_count} chunks, total length: {len(rag_response)}")
            print(f"RAG Response content: {rag_response[:200]}..." if len(rag_response) > 200 else f"RAG Response content: {rag_response}")

            # 2. The rag_response is now the full prompt ready to send to LLM
            reasoning_payload = {
                "model": "llama3:latest",
                "messages": [
                    {
                        "role": "user",
                        "content": rag_response
                    }
                ]
            }
            
            # 3. Send to reasoning API and stream the response
            async with httpx.AsyncClient() as client:
                async with client.stream(
                    "POST", 
                    LLM_API_URL,
                    json=reasoning_payload,
                    timeout=60.0
                ) as response:
                    response.raise_for_status()
                    
                    async for chunk in response.aiter_text():
                        # Process each JSON line from the streaming response
                        for line in chunk.split('\n'):
                            line = line.strip()
                            if line:
                                try:
                                    parsed = json.loads(line)
                                    if parsed.get("message", {}).get("content"):
                                        content = parsed["message"]["content"]
                                        if content:  # Only yield non-empty content
                                            print(f"Yielding content: {content}")
                                            yield f"{json.dumps({'message': {'role': 'assistant', 'content': content}})}\n"
                                except json.JSONDecodeError:
                                    # Skip invalid JSON lines
                                    continue
                                    
        except Exception as e:
            # Send error message as JSON
            yield f"{json.dumps({'error': str(e)})}\n"
    
    return StreamingResponse(
        generate_stream(),
        media_type="text/plain",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"}
    )

@app.get("/")
def health_check():
    return {"status": "running", "message": "RAG API is ready!"}

# --- 4. CHẠY SERVER ---
if __name__ == "__main__":
    import uvicorn
    # Chạy server tại localhost cổng 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
