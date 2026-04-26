# src/ingestion/screen.py
import mss
import numpy as np
import cv2
import time
import os
from datetime import datetime

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
                diff = self._compute_similarity(self.prev_frame, frame)
                # If difference is low (screen didn't change), skip saving
                if diff < 100:  # Threshold needs tuning based on resolution
                    return None

            self.prev_frame = frame
            
            # Save file
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = os.path.join(self.output_dir, f"screen_{timestamp}.png")
            
            # Downscale for storage efficiency (Optional)
            # frame = cv2.resize(frame, (1920, 1080)) 
            
            cv2.imwrite(filename, frame)
            print(f"[Captured] {filename}")
            return filename

if __name__ == "__main__":
    recorder = ScreenRecorder()
    try:
        while True:
            recorder.capture()
            time.sleep(2) # Snap every 2 seconds
    except KeyboardInterrupt:
        print("Stopping recording...")