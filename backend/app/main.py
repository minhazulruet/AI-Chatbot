"""
Main FastAPI Application Entry Point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import logging
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import routers
from app.api import auth, rag, chat, quiz, flashcard, diagnostic
from app.services.db_init import init_all_tables

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle"""
    logger.info("🚀 Application startup")
    
    # Initialize database tables
    await init_all_tables()
    
    yield
    logger.info("🛑 Application shutdown")


# Create FastAPI app
app = FastAPI(
    title="AI Chatbot API",
    description="AI-Powered Chatbot with RAG capabilities",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Basic health check endpoint
@app.get("/")
async def root():
    return {
        "message": "AI Chatbot API is running",
        "version": "1.0.0",
        "status": "healthy"
    }


@app.get("/health")
async def health_check():
    return {"status": "ok"}


# Include routers
app.include_router(auth.router)
app.include_router(rag.router)
app.include_router(chat.router)
app.include_router(quiz.router)
app.include_router(flashcard.router)
app.include_router(diagnostic.router)

# Serve static frontend files
frontend_path = os.path.join(os.path.dirname(__file__), "../../frontend")
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="static")

# TODO: Import and include other routers
# from app.api import quiz, flashcards, diagnostics, circuit_solver
# app.include_router(quiz.router)
# app.include_router(flashcards.router)
# app.include_router(diagnostics.router)
# app.include_router(circuit_solver.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
