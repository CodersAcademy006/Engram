# src/memory/store.py
import lancedb
from sentence_transformers import SentenceTransformer
import os
import time

class MemoryStore:
    def __init__(self, db_path="data/ghost.db"):
        print("🧠 Loading Embedding Model (all-MiniLM-L6-v2)...")
        # This model turns text into numbers (vectors)
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Connect to LanceDB (it creates the folder if it's missing)
        self.db = lancedb.connect(db_path)
        
        # Create or Open the table
        if "memories" not in self.db.table_names():
            print("Creating new vector table...")
            # We insert one dummy row to define the schema automatically
            dummy_data = [{
                "vector": self.embedding_model.encode("hello world"),
                "text": "hello world",
                "timestamp": time.time(),
                "source": "test",
                "filepath": "none"
            }]
            self.table = self.db.create_table("memories", data=dummy_data)
        else:
            self.table = self.db.open_table("memories")

    def add_memory(self, text, source, filepath):
        """
        Saves text into the database.
        """
        if not text or len(text) < 5: 
            return # Skip tiny noise
            
        print(f"  [Memory] Indexing: {text[:30]}...")
        
        vector = self.embedding_model.encode(text)
        
        data = [{
            "vector": vector,
            "text": text,
            "timestamp": time.time(),
            "source": source,
            "filepath": filepath
        }]
        
        self.table.add(data)

    def search(self, query, limit=5):
        """
        Finds the most relevant memories for a question.
        """
        print(f"🔍 Searching for: '{query}'")
        query_vec = self.embedding_model.encode(query)
        
        # LanceDB search
        results = self.table.search(query_vec).limit(limit).to_list()
        return results

# --- Manual Test ---
if __name__ == "__main__":
    # When you run this file directly, it tests the database.
    memory = MemoryStore()
    
    # 1. Add fake data
    print("Adding test data...")
    memory.add_memory("The password for the server is 12345", "screen", "img1.png")
    
    # 2. Search for it (using different words)
    print("\nTesting Search...")
    results = memory.search("what is the server password?")
    
    for r in results:
        print(f"Match: {r['text']} (Source: {r['source']})")