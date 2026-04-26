# src/ingestion/audio.py
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import os
import time
from datetime import datetime
import io
from src.utils.encryption import encrypt_data

class AudioRecorder:
    def __init__(self, output_dir="data/audio_chunks", sample_rate=16000, duration=30, threshold=0.01):
        """
        duration: Seconds per chunk
        threshold: RMS amplitude threshold for silence detection (0.0 to 1.0)
        """
        self.output_dir = output_dir
        self.sample_rate = sample_rate
        self.duration = duration
        self.threshold = threshold
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def is_silent(self, data):
        """Returns True if the RMS amplitude is below the threshold."""
        # Calculate RMS (Root Mean Square) amplitude
        rms = np.sqrt(np.mean(data**2))
        return rms < self.threshold

    def record_chunk(self):
        print(f"🎤 Listening for {self.duration}s...")
        
        # Record audio
        recording = sd.rec(
            int(self.duration * self.sample_rate), 
            samplerate=self.sample_rate, 
            channels=1,
            dtype='float32' # float32 is standard for Whisper
        )
        sd.wait()  # Wait until recording is finished
        
        # Check silence
        if self.is_silent(recording):
            print("Silence detected... (discarded)")
            return None
        
        # Write to an in-memory buffer
        buffer = io.BytesIO()
        wav.write(buffer, self.sample_rate, recording)
        buffer.seek(0)
        audio_bytes = buffer.read()
        
        # Encrypt the audio data
        encrypted_data = encrypt_data(audio_bytes)
        
        # Save encrypted data to file
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = os.path.join(self.output_dir, f"audio_{timestamp}.wav.enc") # Add .enc extension
        
        with open(filename, "wb") as f:
            f.write(encrypted_data)
            
        print(f"[Saved & Encrypted Audio] {filename}")
        return filename

if __name__ == "__main__":
    from config import Config
    from src.utils.logger import logger
    recorder = AudioRecorder(
        output_dir=Config.AUDIO_CHUNKS_DIR,
        sample_rate=Config.AUDIO_SAMPLE_RATE,
        duration=Config.AUDIO_CHUNK_DURATION
    )
    try:
        while True:
            recorder.record_chunk()
    except KeyboardInterrupt:
        print("\nStopping audio...")