# src/processing/vision.py
import os
import time
import easyocr
# This import connects the "Eye" to the "Memory"
from src.memory.store import MemoryStore

import os
import time
import easyocr
import cv2
import numpy as np
from src.memory.store import MemoryStore
from src.utils.encryption import decrypt_data
from config import Config
from src.utils.logger import logger

class ImageProcessor:
    def __init__(self, input_dir=Config.SCREENSHOTS_DIR):
        logger.info("👁️ Loading EasyOCR model (this may take a minute on first run)...")
        self.reader = easyocr.Reader(['en'], gpu=False) 
        self.input_dir = input_dir
        self.memory = MemoryStore()

    def process_file(self, filepath):
        logger.info(f"👁️ Processing encrypted file: {filepath}")
        
        try:
            # 1. Read and decrypt the file
            with open(filepath, 'rb') as f:
                encrypted_data = f.read()
            
            decrypted_data = decrypt_data(encrypted_data)
            
            # If decryption fails or isn't enabled, data might be raw image bytes
            if decrypted_data == encrypted_data and not Config.ENCRYPTION_ENABLED:
                 logger.warning("Decryption skipped or failed, processing as raw data.")
            
            # 2. Decode image in memory
            image_np = np.frombuffer(decrypted_data, np.uint8)
            img = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
            
            if img is None:
                logger.error(f"  [Error] Failed to decode image from {filepath}. It may be corrupted or not a valid image.")
                return None

            # 3. Run OCR
            results = self.reader.readtext(img, detail=0)
            full_text = " ".join(results)
            
            if not full_text.strip():
                logger.info("  -> No text found, skipping.")
                # We still create the .txt file to mark it as processed
                txt_path = filepath.replace(".png.enc", ".txt")
                with open(txt_path, "w", encoding="utf-8") as f:
                    f.write("")
                return None
                
            logger.info(f"  -> Found text: '{full_text[:50]}...'")
            
            # 4. Save transcript locally to mark as processed
            txt_path = filepath.replace(".png.enc", ".txt")
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(full_text)
            
            # 5. Index into Vector Database
            self.memory.add_memory(full_text, "screen", filepath)
                
            return full_text
            
        except Exception as e:
            logger.error(f"  [Error] Failed to process image {filepath}: {e}", exc_info=True)
            return None

    def run_loop(self):
        logger.info("👁️ Vision Processor Service Started")
        while True:
            try:
                files = [f for f in os.listdir(self.input_dir) if f.endswith(".png.enc")]
                
                for file in files:
                    enc_path = os.path.join(self.input_dir, file)
                    txt_path = enc_path.replace(".png.enc", ".txt")
                    
                    if not os.path.exists(txt_path):
                        self.process_file(enc_path)
                
                time.sleep(5)
            except Exception as e:
                logger.error(f"👁️ Vision Processor loop failed: {e}", exc_info=True)
                time.sleep(15) # Sleep longer on failure


if __name__ == "__main__":
    processor = ImageProcessor()
    processor.run_loop()