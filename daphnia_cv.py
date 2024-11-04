import cv2
import numpy as np
from tkinter import Tk, filedialog
import os

def filter_image(frame):
    """
    Apply color filtering to a single frame using vectorized operations.
    
    Args:
    frame (numpy.ndarray): Input image frame
    
    Returns:
    numpy.ndarray: Filtered frame with white pixels where conditions are met
    """
    # Calculate the difference between channels
    r_g_diff = np.abs(frame[:, :, 2] - frame[:, :, 1])
    g_b_diff = np.abs(frame[:, :, 1] - frame[:, :, 0])
    
    # Create a mask where both conditions are met
    mask = (r_g_diff < 16) & (g_b_diff < 16)
    filtered_frame = np.where(mask[..., None], 255, frame)
    
    return filtered_frame.astype(np.uint8), mask.astype(np.uint8) * 255

def select_video_file():
    """
    Opens a file dialog for video selection.
    
    Returns:
    str: Path to selected video file
    """
    root = Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(
        title="Select Video File",
        filetypes=[
            ("Video files", "*.mov *.mp4 *.avi"),
            ("All files", "*.*")
        ]
    )
    return file_path

def main():
    vid_path = select_video_file()
    
    if not vid_path:  # User cancelled selection
        print("No file selected. Exiting...")
        return
    
    video = cv2.VideoCapture(vid_path)
    
    if not video.isOpened():
        print(f"Error: Could not open video file at {vid_path}")
        return
    
    ret, first_frame = video.read()
    
    if not ret:
        print("Error: Could not read the first frame.")
        video.release()
        return
    
    scale_factor = 0.3
    scaled_first_frame = cv2.resize(first_frame, (0, 0), fx=scale_factor, fy=scale_factor)
    
    bounding_box = cv2.selectROI("Select Daphnia Environment", scaled_first_frame, showCrosshair=True)
    cv2.destroyWindow("Select Daphnia Environment")
    x, y, w, h = map(int, bounding_box)
    
    top, bottom, left, right = int(y/scale_factor), int((y + h)/scale_factor), int(x/scale_factor), int((x + w)/scale_factor)
    print(f"ROI coordinates - Top: {top}, Bottom: {bottom}, Left: {left}, Right: {right}")
    
    last_position = None
    total_distance = 0
    counter = 0
    last_cropped_frame = None
    frame_skip = 10
    
    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            break
        
        if counter % frame_skip != 0:
            counter += 1
            continue
        
        cropped_frame = frame[top:bottom, left:right]
        filtered_frame, mask = filter_image(cropped_frame)
        
        gray = cv2.cvtColor(filtered_frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        _, mask = cv2.threshold(blurred, 180, 255, cv2.THRESH_BINARY_INV)
        
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        valid_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 5]
        
        if valid_contours:
            largest_contour = max(valid_contours, key=cv2.contourArea)
            M = cv2.moments(largest_contour)
            
            if M['m00'] > 0:
                cx, cy = int(M['m10'] / M['m00']), int(M['m01'] / M['m00'])
                if last_position:
                    distance = np.sqrt((cx - last_position[0]) ** 2 + (cy - last_position[1]) ** 2)
                    
                    if distance > 100:
                        continue
                    else:
                        total_distance += distance
                        last_position = (cx, cy)
                else:
                    last_position = (cx, cy)
        
        #after every second of video
        if counter % 60 == 0:
            print(f"Total distance is now {total_distance:.4f}")
        
        counter += 1
    
    video.release()
    print(f"Total locomotion distance: {total_distance:.4f} pixels")

if __name__ == "__main__":
    main()