# src/api/rag.py
import ollama
from src.memory.store import MemoryStore

class GhostBrain:
    def __init__(self):
        self.memory = MemoryStore()
        self.model = "llama3.2:3b"

    def ask(self, query):
        """
        Returns a tuple: (answer_text, list_of_source_documents)
        """
        # 1. RETRIEVE
        results = self.memory.search(query, limit=3)
        
        if not results:
            return "I couldn't find any relevant memories locally.", []

        # 2. AUGMENT
        context = ""
        for i, r in enumerate(results):
            source_type = r['source'].upper()
            text = r['text']
            context += f"[{i+1}] Source: {source_type} | Content: {text}\n"

        # 3. GENERATE
        prompt = f"""
        You are GhostOS. Answer based ONLY on the context.
        CONTEXT:
        {context}
        USER QUESTION: 
        {query}
        ANSWER:
        """
        
        try:
            response = ollama.chat(model=self.model, messages=[
                {'role': 'user', 'content': prompt},
            ])
            return response['message']['content'], results
        except Exception as e:
            return f"Error talking to Ollama: {e}", []

if __name__ == "__main__":
    # Test
    brain = GhostBrain()
    ans, sources = brain.ask("test")
    print(ans)
    print(sources)