# src/processing/speech.py
import os
import time
from faster_whisper import WhisperModel
# This import connects the "Ear" to the "Memory"
from src.memory.store import MemoryStore

import os
import time
import io
from faster_whisper import WhisperModel
from src.memory.store import MemoryStore
from src.utils.encryption import decrypt_data
from config import Config
from src.utils.logger import logger

class AudioProcessor:
    def __init__(self, input_dir=Config.AUDIO_CHUNKS_DIR, model_size="tiny.en"):
        logger.info(f"🎧 Loading Whisper model: {model_size}...")
        self.model = WhisperModel(model_size, device="cpu", compute_type="int8")
        self.input_dir = input_dir
        self.memory = MemoryStore()

    def process_file(self, filepath):
        logger.info(f"🎧 Processing encrypted audio: {filepath}")
        
        try:
            # 1. Read and decrypt the file
            with open(filepath, 'rb') as f:
                encrypted_data = f.read()
            
            decrypted_data = decrypt_data(encrypted_data)

            # If decryption fails or isn't enabled, data might be raw audio bytes
            if decrypted_data == encrypted_data and not Config.ENCRYPTION_ENABLED:
                 logger.warning("Decryption skipped or failed, processing as raw data.")

            # 2. Load decrypted data into an in-memory buffer
            audio_buffer = io.BytesIO(decrypted_data)
            
            # 3. Run transcription on the buffer
            segments, info = self.model.transcribe(audio_buffer, beam_size=5)
            full_text = " ".join([segment.text for segment in segments]).strip()
            
            # 4. Save transcript locally to mark as processed
            txt_path = filepath.replace(".wav.enc", ".txt")
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(full_text)

            if not full_text:
                logger.info("  -> No speech detected.")
                return None

            logger.info(f"  -> Detected: '{full_text[:50]}...'")
                
            # 5. Index into Vector Database
            self.memory.add_memory(full_text, "audio", filepath)
                
            return full_text
            
        except Exception as e:
            logger.error(f"  [Error] Failed to transcribe audio {filepath}: {e}", exc_info=True)
            return None

    def run_loop(self):
        """Continuous loop to process new files"""
        logger.info("🎧 Audio Processor Service Started")
        while True:
            try:
                files = [f for f in os.listdir(self.input_dir) if f.endswith(".wav.enc")]
                
                for file in files:
                    enc_path = os.path.join(self.input_dir, file)
                    txt_path = enc_path.replace(".wav.enc", ".txt")
                    
                    if not os.path.exists(txt_path):
                        self.process_file(enc_path)
                
                time.sleep(5)
            except Exception as e:
                logger.error(f"🎧 Audio Processor loop failed: {e}", exc_info=True)
                time.sleep(15) # Sleep longer on failure


if __name__ == "__main__":
    processor = AudioProcessor()
    processor.run_loop()