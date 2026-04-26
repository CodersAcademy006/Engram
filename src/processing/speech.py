# src/processing/speech.py
import os
import time
from faster_whisper import WhisperModel
# This import connects the "Ear" to the "Memory"
from src.memory.store import MemoryStore

class AudioProcessor:
    def __init__(self, input_dir="data/audio_chunks", model_size="tiny.en"):
        # "tiny.en" is fast. Use "small" or "medium" if you want better accuracy later.
        print(f"🎧 Loading Whisper model: {model_size}...")
        self.model = WhisperModel(model_size, device="cpu", compute_type="int8")
        self.input_dir = input_dir
        
        # Initialize the connection to the Vector Database
        self.memory = MemoryStore()

    def process_file(self, filepath):
        print(f"Transcribing {filepath}...")
        
        try:
            # Run transcription
            segments, info = self.model.transcribe(filepath, beam_size=5)
            
            # Combine segments into one string
            full_text = " ".join([segment.text for segment in segments]).strip()
            
            if not full_text:
                print("  -> No speech detected.")
                # We still create an empty txt file so we don't re-process it forever
                txt_path = filepath.replace(".wav", ".txt")
                with open(txt_path, "w", encoding="utf-8") as f:
                    f.write("")
                return None

            print(f"  -> Detected: '{full_text[:50]}...'")
            
            # 1. Save transcript locally
            txt_path = filepath.replace(".wav", ".txt")
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(full_text)
                
            # 2. Index into Vector Database
            self.memory.add_memory(full_text, "audio", filepath)
                
            return full_text
            
        except Exception as e:
            print(f"  [Error] Failed to transcribe audio: {e}")
            return None

    def run_loop(self):
        """Continuous loop to process new files"""
        print("🎧 Audio Processor Service Started")
        while True:
            # Find all .wav files
            files = [f for f in os.listdir(self.input_dir) if f.endswith(".wav")]
            
            for file in files:
                wav_path = os.path.join(self.input_dir, file)
                txt_path = wav_path.replace(".wav", ".txt")
                
                # If .txt doesn't exist, we process it
                if not os.path.exists(txt_path):
                    self.process_file(wav_path)
            
            time.sleep(5)  # Check every 5 seconds

if __name__ == "__main__":
    processor = AudioProcessor()
    processor.run_loop()