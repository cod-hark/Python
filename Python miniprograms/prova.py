import cv2
import numpy as np
import pyautogui
import time
import os

# Set the output filename
output_filename = "screen_recording.mp4"

# Set the screen region to record (e.g., a 640x480 region)
screen_width, screen_height = 640, 480
resolution = (screen_width, screen_height)

# Set the frames per second (FPS) for the recording
fps = 30.0

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*"XVID")
out = cv2.VideoWriter(output_filename, fourcc, fps, resolution)

# Define the recording duration in seconds
recording_duration = 5

# Start the screen recording
start_time = time.time()
try:
    while True:
        # Capture the screen (only the defined region)
        screen = pyautogui.screenshot(region=(0, 0, screen_width, screen_height))

        # Convert the screenshot to a numpy array and BGR format for OpenCV
        frame = np.array(screen)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # Write the frame to the output video
        out.write(frame)

        # Stop recording after the specified duration
        if time.time() - start_time > recording_duration:
            break

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Release the VideoWriter object
    out.release()

    # Inform the user that recording is finished
    print(f"Recording finished. Video saved as {output_filename}.")