from ultralytics import YOLO
import cv2

# Cargar el modelo YOLOv8 entrenado desde una ruta local relativa
model = YOLO('modelo-chalecos/exp13/weights/best.pt')

# Inicializar la cámara (0 = cámara web por defecto)
cap = cv2.VideoCapture(0)

# Verifica si la cámara se abrió correctamente
if not cap.isOpened():
    print("❌ No se pudo abrir la cámara.")
    exit()

while True:
    # Leer un frame de la cámara
    ret, frame = cap.read()
    if not ret:
        print("⚠️ No se pudo leer el frame.")
        break

    # Realizar la detección sobre el frame (confianza mínima de 0.5)
    results = model.predict(source=frame, conf=0.5, imgsz=640, stream=True)

    # Dibujar las predicciones sobre el frame original
    for r in results:
        annotated_frame = r.plot()  # Dibuja cajas y etiquetas

        # Mostrar el frame en una ventana
        cv2.imshow("YOLOv8 - Webcam", annotated_frame)

    # Salir con la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la cámara y cerrar ventanas
cap.release()
cv2.destroyAllWindows()
