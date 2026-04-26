# Ghost-OS: Your Personal AI Memory System

## The Manifesto

Ghost-OS is a privacy-first, local-first AI system that acts as your digital memory. It continuously captures what you see and hear, processes it intelligently, and allows you to query your past experiences using natural language.

**Core Principles:**
- 🔒 **Privacy First**: All data stays on your machine
- 🧠 **AI-Powered**: OCR, speech recognition, and semantic search
- ⚡ **Real-time**: Continuous capture and processing
- 🎯 **Simple**: Easy to set up and use

## Architecture

```
EYES & EARS (Ingestion) → BRAIN (Processing) → HIPPOCAMPUS (Memory) → MOUTH (API)
```

## Setup Guide

### Prerequisites
- Python 3.9+
- At least 8GB RAM
- 10GB+ free disk space

### Installation

1. Clone and navigate to the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure your environment:
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. Run Ghost-OS:
   ```bash
   python main.py
   ```

## Development Roadmap

- **WEEK 1**: Eyes and Ears (Screen & Audio Capture)
- **WEEK 2**: Brain (OCR, Transcription, Embedding)
- **WEEK 3**: Mouth (RAG & Query API)
- **WEEK 4**: Face (UI Dashboard)

## License

MIT License - Use responsibly and ethically.
