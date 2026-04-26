# I Built a "Microsoft Recall" Alternative That Runs 100% Locally (with Llama 3 & Python)

When Microsoft announced Recall, I loved the concept:  
"Ctrl+F for your entire digital life."  
Imagine asking your computer,  
*“What was that error stack trace I saw 2 hours ago?”*  
or  
*“What did the client say about the budget in last Tuesday's meeting?”*  
and getting an instant answer.

But there was a catch. **The Privacy Nightmare.**  
Sending screenshots of my bank accounts, private chats, and code to the cloud (or having them stored in a closed-source black box) was a dealbreaker.

So, I decided to build my own.  
Meet **Engram** (formerly Ghost-OS): An open-source, privacy-first AI memory agent.

It records your screen and audio, indexes everything on your device, and lets you chat with your history using Llama 3.2.  
**No data leaves your laptop.**

Here is how I built it using Python, LanceDB, and Ollama.

---

## 🏗️ The Architecture

The system is designed as an **Event-Driven Multimodal Pipeline**.  
It needed to be lightweight enough to run in the background without killing my CPU.

The pipeline has 4 stages:

1. **The Senses (Ingestion):** Capturing Screen (`mss`) and Audio (`sounddevice`).
2. **The Brain (Processing):** Extracting text using OCR (`EasyOCR`) and Transcription (`Faster-Whisper`).
3. **The Memory (Storage):** Embedding text into a local Vector DB (`LanceDB`).
4. **The Voice (Retrieval):** A RAG pipeline using Ollama (Llama 3.2).

---

### 1. The "Senses": Deduplication is Key

Recording the screen every 2 seconds creates massive data bloat.  
Most of the time, your screen is static (while reading or coding).

To solve this, I implemented **SSIM (Structural Similarity Index)** checks.  
We only save a new frame if the screen content has changed significantly.

```python
# src/ingestion/screen.py snippet
def capture(self):
    sct_img = self.sct.grab(self.monitor)
    frame = np.array(sct_img)
    
    # Compare with previous frame using Mean Squared Error
    if self.prev_frame is not None:
        diff = np.sum((frame - self.prev_frame) ** 2)
        if diff < threshold:
            return None # Skip static screens

    self.prev_frame = frame
    cv2.imwrite(filename, frame)
```

---

### 2. The "Memory": Why LanceDB?

I needed a Vector Database, but running a Docker container for Postgres/pgvector or Pinecone felt like overkill for a local tool.

I chose **LanceDB**.  
It’s serverless (runs as a file, like SQLite), incredibly fast, and handles multimodal data easily.

```python
# src/memory/store.py
import lancedb
from sentence_transformers import SentenceTransformer

class MemoryStore:
    def __init__(self):
        self.db = lancedb.connect("data/engram.db")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def add_memory(self, text, source, filepath):
        vector = self.model.encode(text)
        self.table.add([{
            "vector": vector,
            "text": text,
            "source": source,
            "timestamp": time.time()
        }])
```

---

### 3. The "Voice": RAG with Llama 3

This is where the magic happens.  
When you ask Engram a question, it doesn't just guess.  
It performs **Retrieval Augmented Generation (RAG)**.

- It converts your question into a vector.
- It queries LanceDB for the top 3 most relevant screenshots or transcripts.
- It feeds those snippets to Llama 3.2 (running locally via Ollama) to generate the answer.

```python
# src/api/rag.py
def ask(self, query):
    # 1. Retrieve Context
    results = self.memory.search(query, limit=3)
    
    context = ""
    for r in results:
        context += f"Source: {r['source']} | Content: {r['text']}\n"

    # 2. Generate Answer via Ollama
    prompt = f"Based on this context:\n{context}\nAnswer: {query}"
    
    response = ollama.chat(model="llama3.2:3b", messages=[
        {'role': 'user', 'content': prompt}
    ])
    return response['message']['content']
```

---

## ⚡ The Result

The result is a Streamlit dashboard that feels like a superpower.

I can work for 4 hours, forget where I saw a specific API key, ask Engram  
*"Where is the Stripe key?"*, and it pulls up the exact frame from 3 hours ago.

---

### Privacy Check:

- All data stored in `./data` (hidden locally).
- No API keys required.
- Works offline (Air-gapped friendly).

---

## 🚀 Try it yourself

The project is **Open Source**.  
You can clone it, audit the code, and run it on your own machine today.

🔗 GitHub Repo: [INSERT YOUR GITHUB REPO LINK HERE]

I’m actively looking for contributors!  
If you want to help add features like PII redaction or Video support, drop a PR.

---

**Tech Stack:** Python 3.11, Streamlit, Ollama, LanceDB, EasyOCR, Faster-Whisper.
