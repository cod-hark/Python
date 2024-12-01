

##[Running] /usr/bin/python3 "d:\pau\informatica\VS-Git\Python\Python miniprograms\Screen Recorder.py"
#El sistema no puede encontrar la ruta especificada.






# mejoras--> automatico o estableciendo los parametros
#Create a Screen recorder using Python
# cv2: Es parte de OpenCV, una biblioteca para procesamiento de imágenes y videos. Se usa para codificar y escribir el video resultante.
#numpy: Es una biblioteca para trabajar con matrices y realizar cálculos numéricos de manera eficiente. Se utiliza aquí para convertir la imagen de captura en un formato compatible con OpenCV.
#pyautogui: Sirve para tomar capturas de pantalla y para automatizar tareas como mover el ratón o escribir en el teclado.
#time: Se utiliza para medir el tiempo de grabación (controlar la duración del video).

import cv2
import numpy as np
import pyautogui
import time
import os

print(os.getcwd())  # Esto imprime la ruta actual del script

output_folder = "C:/Users/Pau/Desktop/screen_recording.mp4"
#if not os.path.exists(output_folder):
#    os.makedirs(output_folder)  # Crea el directorio si no existe

#output_filename = output_folder + "screen_recording.mp4"


#output_filename = os.path.join(os.getcwd(), "screen_recording.mp4")

output_filename = "screen_recording.mp4"


# Set the screen resolution to record
screen_width, screen_height = pyautogui.size()
resolution = (screen_width, screen_height)

# Set the output video filename
output_filename = "screen_recording.mp4"

# Set the frames per second (FPS) for the recording
fps = 30.0

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter(output_filename, fourcc, fps, resolution)

# Define the recording duration in seconds
recording_duration = 5  # Change this to the desired recording duration

# Start the screen recording
start_time = time.time()
while True:
    # Capture the screen
    screen = pyautogui.screenshot()

    # Convert the screenshot to a numpy array and BGR format for OpenCV
    frame = np.array(screen)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    # Write the frame to the output video
    out.write(frame)

    # Stop recording after the specified duration
    if time.time() - start_time > recording_duration:
        break

# Release the VideoWriter object
out.release()

# Optional: Inform the user that recording is finished
print(f"Recording finished. Video saved as {output_filename}.")
