from multiquery import query

# server.py
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import ollama
import json



# --- 1. SETUP RAG (Copy phần khởi tạo từ code cũ của bạn vào đây) ---
# Ví dụ giả định bạn đã có biến 'index' (Pinecone) và 'encoder' sẵn sàng
# from my_rag_module import index, encoder 
# (Hoặc paste code khởi tạo index/encoder vào đây)

app = FastAPI()

# Add CORS middleware to handle OPTIONS requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Next.js dev server
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# Định nghĩa cấu trúc dữ liệu đầu vào
class QueryRequest(BaseModel):
    question: str

# --- 3. ĐỊNH NGHĨA API ENDPOINT ---
@app.post("/api/chat")
async def chat_endpoint(request: QueryRequest):
    """
    API nhận câu hỏi -> Chạy RAG -> Trả về câu trả lời streaming
    """
    print(request.question)
    
    async def generate_stream():
        try:
            # Get the response generator from query function
            response_generator = query(request.question, stream=True)
            
            for chunk in response_generator:
                # Yield each chunk as JSON in Server-Sent Events format
                yield f"data: {json.dumps({'content': chunk})}\n\n"
                
        except Exception as e:
            # Send error message as JSON
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
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
