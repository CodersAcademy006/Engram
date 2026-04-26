import subprocess
import time
import sys
import signal
import os

# Keep track of processes so we can kill them later
processes = []

def stream_logs(process, prefix):
    """Optional: Print logs from subprocesses if you want to see them all in one place"""
    for line in iter(process.stdout.readline, b''):
        print(f"[{prefix}] {line.decode().strip()}")

def cleanup(sig, frame):
    print("\n🛑 Shutting down Ghost-OS Ecosystem...")
    for p in processes:
        if p.poll() is None:  # If process is still running
            if sys.platform == "win32":
                p.send_signal(signal.CTRL_C_EVENT) # Try graceful first
                time.sleep(1)
                p.terminate() # Force kill if needed
            else:
                p.terminate()
    print("✅ All services stopped.")
    sys.exit(0)

def main():
    # Register Ctrl+C handler
    signal.signal(signal.SIGINT, cleanup)

    print("👻 Ghost-OS Starting...")
    print("----------------------")

    # 1. Start Ingestion (Screen & Audio Recorder)
    print("🚀 Launching Ingestion Engine (main.py)...")
    p_ingest = subprocess.Popen([sys.executable, "main.py"])
    processes.append(p_ingest)

    # 2. Start Vision Processor
    print("👁️ Launching Vision Processor...")
    p_vision = subprocess.Popen([sys.executable, "src/processing/vision.py"])
    processes.append(p_vision)

    # 3. Start Audio Processor
    print("🎧 Launching Audio Processor...")
    p_audio = subprocess.Popen([sys.executable, "src/processing/speech.py"])
    processes.append(p_audio)

    # 4. Start Streamlit UI
    print("🎨 Launching UI...")
    # Streamlit runs as a separate command
    p_ui = subprocess.Popen(["streamlit", "run", "ui/app.py"])
    processes.append(p_ui)

    print("----------------------")
    print("✅ All Systems Online.")
    print("👉 Open your browser at http://localhost:8501")
    print("Press Ctrl+C to stop everything.")

    # Keep the main script alive to monitor processes
    while True:
        time.sleep(1)
        # Optional: Check if any critical process died and restart it?
        if p_ui.poll() is not None:
            print("❌ UI crashed or closed. Exiting.")
            cleanup(None, None)

if __name__ == "__main__":
    main()