"""
FastAPI Routes
REST API endpoints for querying Ghost-OS
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from loguru import logger

from config import Config
# from src.api.rag import RAGSystem

app = FastAPI(title="Ghost-OS API", version="1.0.0")


class QueryRequest(BaseModel):
    """Query request model"""
    query: str
    top_k: int = 5


class QueryResponse(BaseModel):
    """Query response model"""
    answer: str
    sources: list
    metadata: dict


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "message": "Ghost-OS API is running",
        "version": "1.0.0"
    }


@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """Query endpoint - RAG-based search"""
    try:
        logger.info(f"Received query: {request.query}")
        
        # TODO: Implement RAG system
        # rag = RAGSystem()
        # result = rag.query(request.query, top_k=request.top_k)
        
        return QueryResponse(
            answer="Placeholder answer",
            sources=[],
            metadata={"query": request.query}
        )
        
    except Exception as e:
        logger.error(f"Query error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stats")
async def stats():
    """Get system statistics"""
    return {
        "screenshots_captured": 0,
        "audio_chunks_recorded": 0,
        "total_embeddings": 0,
        "storage_used_mb": 0
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=Config.API_HOST, port=Config.API_PORT)
