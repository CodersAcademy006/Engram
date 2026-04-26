"""
Ghost-OS Central Configuration
All paths, intervals, and settings are defined here
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Central configuration for Ghost-OS"""
    
    # Base paths
    BASE_DIR = Path(__file__).parent
    DATA_DIR = BASE_DIR / "data"
    SCREENSHOTS_DIR = DATA_DIR / "screenshots"
    AUDIO_CHUNKS_DIR = DATA_DIR / "audio_chunks"
    DB_DIR = DATA_DIR / "db"
    
    # Ensure directories exist
    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    AUDIO_CHUNKS_DIR.mkdir(parents=True, exist_ok=True)
    DB_DIR.mkdir(parents=True, exist_ok=True)
    
    # Ingestion settings
    SCREEN_CAPTURE_ENABLED = os.getenv("SCREEN_CAPTURE_ENABLED", "true").lower() == "true"
    SCREEN_CAPTURE_INTERVAL = int(os.getenv("SCREEN_CAPTURE_INTERVAL", "5"))  # seconds
    SSIM_THRESHOLD = float(os.getenv("SSIM_THRESHOLD", "0.95"))  # Similarity threshold
    
    AUDIO_CAPTURE_ENABLED = os.getenv("AUDIO_CAPTURE_ENABLED", "true").lower() == "true"
    AUDIO_SAMPLE_RATE = int(os.getenv("AUDIO_SAMPLE_RATE", "16000"))  # Hz
    AUDIO_CHUNK_DURATION = int(os.getenv("AUDIO_CHUNK_DURATION", "30"))  # seconds
    
    # Processing settings
    OCR_ENABLED = os.getenv("OCR_ENABLED", "true").lower() == "true"
    TRANSCRIPTION_ENABLED = os.getenv("TRANSCRIPTION_ENABLED", "true").lower() == "true"
    PII_REDACTION_ENABLED = os.getenv("PII_REDACTION_ENABLED", "false").lower() == "true"
    
    # Memory settings
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    VECTOR_DB_TYPE = os.getenv("VECTOR_DB_TYPE", "lancedb")  # lancedb or chromadb
    
    # API settings
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", "8000"))
    
    # Security
    ENCRYPTION_ENABLED = os.getenv("ENCRYPTION_ENABLED", "false").lower() == "true"
    ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", "")
    
    # LLM settings (for RAG)
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama")  # ollama, openai, etc.
    LLM_MODEL = os.getenv("LLM_MODEL", "llama2")
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
