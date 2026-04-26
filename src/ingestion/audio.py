# src/ingestion/audio.py
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import os
import time
from datetime import datetime

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
            print("creating silence... (discarded)")
            return None
        
        # Save file
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = os.path.join(self.output_dir, f"audio_{timestamp}.wav")
        
        # Scipy expects int16 or float32. We recorded in float32.
        wav.write(filename, self.sample_rate, recording)
        print(f"[Saved Audio] {filename}")
        return filename

if __name__ == "__main__":
    recorder = AudioRecorder(duration=10) # 10s chunks for testing
    try:
        while True:
            recorder.record_chunk()
    except KeyboardInterrupt:
        print("\nStopping audio...")