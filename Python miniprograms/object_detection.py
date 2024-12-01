import torch
import cv2

# Cargar el modelo YOLOv5 preentrenado
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Lista para almacenar rastreadores y las cajas de límite correspondientes
trackers = []

# Definir una función para realizar la detección de objetos
def detect_objects(frame):
    # Realizar detección en el frame actual
    results = model(frame)
    
    # Extraer los objetos detectados y sus coordenadas
    detected_objects = results.xyxy[0].numpy()  # Coordenadas de los objetos
    return detected_objects

# Inicializar el seguimiento de los objetos detectados
def initialize_trackers(frame, detected_objects):
    global trackers
    for obj in detected_objects:
        x1, y1, x2, y2, _, _ = obj  # Coordenadas del objeto (x1, y1, x2, y2)
        bbox = (x1, y1, x2 - x1, y2 - y1)  # Convertir las coordenadas a formato de caja
        tracker = cv2.TrackerCSRT_create()  # Usar CSRT tracker
        tracker.init(frame, bbox)  # Inicializar el rastreador con el frame y la caja delimitadora
        trackers.append(tracker)

def process_video(video_path):
    global trackers
    # Capturar el video desde el archivo
    cap = cv2.VideoCapture(video_path)

    while True:
        # Leer el siguiente frame del video
        ret, frame = cap.read()
        if not ret:
            break  # Si no hay más frames, salir del bucle

        # Detectar objetos en el primer frame
        if len(trackers) == 0:  # Si no hay objetos siendo rastreados
            detected_objects = detect_objects(frame)
            initialize_trackers(frame, detected_objects)

        # Actualizar la posición de los objetos rastreados
        new_trackers = []
        for tracker in trackers:
            success, box = tracker.update(frame)
            if success:
                p1 = (int(box[0]), int(box[1]))
                p2 = (int(box[0] + box[2]), int(box[1] + box[3]))
                cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
                new_trackers.append(tracker)
        
        trackers = new_trackers

        # Mostrar el frame con los objetos rastreados
        cv2.imshow("Tracking", frame)

        # Salir del bucle si se presiona la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Liberar recursos
    cap.release()
    cv2.destroyAllWindows()

# Llamar a la función para procesar el video (pon el nombre de tu archivo de video aquí)
#process_video('tu_video.mp4')

# * Procesar video de la camara web
process_video(0)  # 0 se refiere a la cámara web por defecto
