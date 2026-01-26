# CP-Helper

A Competitive Programming assistant powered by Retrieval-Augmented Generation (RAG) with local LLM capabilities. This project provides intelligent assistance for CP problems using VNOI/USACO documentation.

## 🏗️ Architecture

This is a full-stack application with two main components:

- **Backend (api-rag)**: FastAPI-based RAG engine with local LLM processing
- **Frontend (frontend)**: Next.js web interface using assistant-ui

## 🚀 Features

- **Semantic Chunking**: Context-aware document splitting using Semantic Router
- **Local LLM**: Meta Llama 3 running via Ollama for privacy and cost efficiency  
- **Vector Search**: Pinecone serverless vector database with high-quality embeddings
- **Real-time Chat**: Streaming responses with modern React UI
- **Multi-language Support**: Optimized for Vietnamese CP documentation

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI (Python 3.10+)
- **LLM**: Meta Llama 3 (local via Ollama)
- **Vector DB**: Pinecone Serverless Index
- **Embeddings**: nomic-ai/nomic-embed-text-v1.5 (768 dim)
- **Chunking**: Semantic Router with rolling window splitting
- **Processing**: LangChain integration

### Frontend
- **Framework**: Next.js 16 with React 19
- **UI Components**: assistant-ui, Radix UI
- **Styling**: Tailwind CSS
- **AI Integration**: Vercel AI SDK
- **TypeScript**: Full type safety

## 📋 Prerequisites

- Python 3.10+
- Node.js 18+
- Ollama installed and running
- Pinecone account and API key

## 🛠️ Installation & Setup

### Backend Setup

1. Navigate to the backend directory:
```bash
cd api-rag
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your Pinecone API key and other configurations
```

5. Start Ollama and pull Llama 3:
```bash
ollama serve
ollama pull llama3
```

6. Run the backend server:
```bash
python server.py
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
# or
pnpm install
```

3. Set up environment variables:
```bash
cp .env.example .env.local
# Edit with your API keys if needed
```

4. Run the development server:
```bash
npm run dev
# or
pnpm dev
```

5. Open [http://localhost:3000](http://localhost:3000) in your browser.

## 📁 Project Structure

```
CP-Helper/
├── api-rag/                  # Backend RAG engine
│   ├── server.py            # FastAPI server with chat endpoints
│   ├── indexing.py          # Document indexing and chunking
│   ├── multiquery.py        # RAG query processing
│   ├── requirements.txt     # Python dependencies
│   └── .env.example         # Environment variables template
├── frontend/                 # Next.js frontend
│   ├── app/                 # App router pages
│   ├── components/          # React components
│   ├── package.json        # Node.js dependencies
│   ├── tsconfig.json       # TypeScript configuration
│   └── tailwind.config.js  # Tailwind CSS config
├── .gitignore              # Git ignore file
└── README.md              # This file
```

## 🔧 Configuration

### Backend Environment Variables
- `PINECONE_API_KEY`: Your Pinecone API key
- `PINECONE_INDEX_NAME`: Name of your Pinecone index
- `OLLAMA_BASE_URL`: Ollama server URL (default: http://localhost:11434)

### Frontend Environment Variables
- `NEXT_PUBLIC_API_URL`: Backend API URL (default: http://localhost:8000)

## 🤖 Usage

1. Start both backend and frontend servers
2. Open the web interface at http://localhost:3000
3. Ask questions about competitive programming concepts
4. Get intelligent responses based on VNOI/USACO documentation

## 📚 Documentation Sources

The system is designed to work with competitive programming documentation from:
- VNOI (Vietnam Olympiad in Informatics)
- USACO (USA Computing Olympiad)
- CP-Algorithms
- Other CP learning resources

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔍 API Endpoints

### POST /api/chat
Main chat endpoint for querying the RAG system.

**Request:**
```json
{
  "question": "How does binary search work?"
}
```

**Response:** Streaming response with RAG-enhanced answers.

## 🛠️ Development

### Running Tests
```bash
# Backend
cd api-rag
pytest

# Frontend  
cd frontend
npm test
```

### Code Formatting
```bash
# Backend
cd api-rag
black .
isort .

# Frontend
cd frontend
npm run prettier:fix
npm run lint
```

## 🐛 Troubleshooting

### Common Issues

1. **Ollama connection failed**: Make sure Ollama is running and Llama 3 is downloaded
2. **Pinecone connection error**: Verify your API key and index configuration
3. **CORS issues**: Check the CORS settings in `server.py`

### Getting Help

- Check the logs in both backend and frontend
- Ensure all environment variables are properly set
- Verify that Ollama and Pinecone services are accessible

---

Built with ❤️ for the Competitive Programming community