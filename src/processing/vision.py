# src/processing/vision.py
import os
import time
import easyocr
# This import connects the "Eye" to the "Memory"
from src.memory.store import MemoryStore

class ImageProcessor:
    def __init__(self, input_dir="data/screenshots"):
        print("👁️ Loading EasyOCR model (this may take a minute first time)...")
        # 'en' for English. GPU=False ensures it runs on any laptop.
        self.reader = easyocr.Reader(['en'], gpu=False) 
        self.input_dir = input_dir
        
        # Initialize the connection to the Vector Database
        self.memory = MemoryStore()

    def process_file(self, filepath):
        print(f"Scanning {filepath}...")
        
        try:
            # Run OCR
            # detail=0 returns just the list of strings found
            results = self.reader.readtext(filepath, detail=0) 
            
            # Combine all found words into one paragraph
            full_text = " ".join(results)
            
            if not full_text.strip():
                print("  -> No text found (skipping index).")
                return None
                
            print(f"  -> Found text: '{full_text[:50]}...'")
            
            # 1. Save transcript locally (backup)
            txt_path = filepath.replace(".png", ".txt")
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(full_text)
            
            # 2. Index into Vector Database (The Magic Step)
            self.memory.add_memory(full_text, "screen", filepath)
                
            return full_text
            
        except Exception as e:
            print(f"  [Error] Failed to process image: {e}")
            return None

    def run_loop(self):
        print("👁️ Vision Processor Service Started")
        while True:
            # Look for .png files in the data folder
            files = [f for f in os.listdir(self.input_dir) if f.endswith(".png")]
            
            for file in files:
                png_path = os.path.join(self.input_dir, file)
                txt_path = png_path.replace(".png", ".txt")
                
                # If .txt doesn't exist, it means we haven't processed it yet
                if not os.path.exists(txt_path):
                    self.process_file(png_path)
            
            # Wait 5 seconds before checking for new screenshots
            time.sleep(5)

if __name__ == "__main__":
    processor = ImageProcessor()
    processor.run_loop()