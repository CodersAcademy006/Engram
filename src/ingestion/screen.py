# src/ingestion/screen.py
import mss
import numpy as np
import cv2
import time
import os
from datetime import datetime
from src.utils.encryption import encrypt_data

class ScreenRecorder:
    def __init__(self, output_dir="data/screenshots", similarity_threshold=0.9):
        self.output_dir = output_dir
        self.similarity_threshold = similarity_threshold
        self.prev_frame = None
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def _compute_similarity(self, frame1, frame2):
        # Convert to grayscale for faster comparison
        gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGRA2GRAY)
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGRA2GRAY)
        
        # Simple structural similarity check (MSE is faster for real-time)
        # For production, we might use SSIM, but MSE is good for "did screen change?"
        err = np.sum((gray1.astype("float") - gray2.astype("float")) ** 2)
        err /= float(gray1.shape[0] * gray1.shape[1])
        return err

    def capture(self):
        with mss.mss() as sct:
            # Capture the primary monitor
            monitor = sct.monitors[1]
            sct_img = sct.grab(monitor)
            
            # Convert to numpy array
            frame = np.array(sct_img)
            
            # Check for duplicates
            if self.prev_frame is not None:
                # Using a simple and fast MSE for similarity check
                diff = self._compute_similarity(self.prev_frame, frame)
                if diff < 100:  # This threshold may need tuning
                    return None

            self.prev_frame = frame
            
            # Encode image to memory buffer
            is_success, buffer = cv2.imencode(".png", frame)
            if not is_success:
                print("[Error] Could not encode image to buffer.")
                return None
            
            # Encrypt the image data
            image_bytes = buffer.tobytes()
            encrypted_data = encrypt_data(image_bytes)

            # Save encrypted data to file
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = os.path.join(self.output_dir, f"screen_{timestamp}.png.enc") # Add .enc extension
            
            with open(filename, "wb") as f:
                f.write(encrypted_data)
                
            print(f"[Captured & Encrypted] {filename}")
            return filename

if __name__ == "__main__":
    # Make sure to add config and logger if you run this standalone
    from config import Config
    from src.utils.logger import logger
    recorder = ScreenRecorder(
        output_dir=Config.SCREENSHOTS_DIR, 
        similarity_threshold=Config.SSIM_THRESHOLD
    )
    try:
        while True:
            recorder.capture()
            time.sleep(Config.SCREEN_CAPTURE_INTERVAL)
    except KeyboardInterrupt:
        print("Stopping recording...")