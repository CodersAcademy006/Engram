import threading
import time
import signal
import sys
from src.ingestion.screen import ScreenRecorder
from src.ingestion.audio import AudioRecorder

# Global event to signal threads to stop
stop_event = threading.Event()

def run_screen_recorder():
    """
    Runs the screen capture loop.
    Captures every 2 seconds.
    """
    print("Example: [Screen Thread] Started")
    recorder = ScreenRecorder()
    
    while not stop_event.is_set():
        try:
            recorder.capture()
            # Sleep in small intervals to check stop_event frequently
            for _ in range(20): 
                if stop_event.is_set(): break
                time.sleep(0.1)
        except Exception as e:
            print(f"[Screen Error] {e}")

def run_audio_recorder():
    """
    Runs the audio capture loop.
    Records in 30-second chunks.
    """
    print("Example: [Audio Thread] Started")
    # Using 30s chunks for production (better for Whisper later)
    recorder = AudioRecorder(duration=30) 
    
    while not stop_event.is_set():
        try:
            # Note: This blocks for 30s. 
            # If you hit Ctrl+C, it will finish the current chunk before stopping.
            recorder.record_chunk() 
        except Exception as e:
            print(f"[Audio Error] {e}")

def signal_handler(sig, frame):
    """Handles Ctrl+C to shutdown gracefully"""
    print("\n\n🛑 Shutting down Ghost-OS... (This may take up to 30s for audio to finish)")
    stop_event.set()

if __name__ == "__main__":
    # Register the Ctrl+C handler
    signal.signal(signal.SIGINT, signal_handler)

    print("👻 Ghost-OS Initializing...")
    print("--------------------------------")

    # Create Threads
    screen_thread = threading.Thread(target=run_screen_recorder, name="ScreenThread")
    audio_thread = threading.Thread(target=run_audio_recorder, name="AudioThread")

    # Start Threads
    screen_thread.start()
    audio_thread.start()

    print("✅ System Online. Recording data locally.")
    print("Press Ctrl+C to stop.")

    # Keep the main thread alive to listen for signals
    while not stop_event.is_set():
        time.sleep(1)

    # Wait for threads to finish
    screen_thread.join()
    audio_thread.join()
    print("👋 System Offline.")