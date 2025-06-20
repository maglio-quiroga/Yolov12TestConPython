# app.py
import streamlit as st
import cv2
from ultralytics import YOLO
import pandas as pd
from datetime import datetime
#streamlit run webcam.py --server.port 8888 --- COMANDO DE BASH


# --- Configuración inicial de Streamlit ---
st.set_page_config(page_title="Detección en Vivo", layout="wide")

st.title("📸 YOLOv8 + Streamlit")
st.markdown(
    """
    Esta app captura vídeo de tu webcam, ejecuta YOLOv8 sobre cada frame  
    y muestra tanto el vídeo anotado como estadísticas en tiempo real.
    """
)

# Sidebar para ajustar parámetros
st.sidebar.header("Ajustes")
conf_thres = st.sidebar.slider("Confianza mínima", 0.0, 1.0, 0.5, 0.05)
imgsz = st.sidebar.selectbox("Tamaño de imagen", [320, 480, 640, 800], index=2)

# Carga tu modelo entrenado
@st.cache_resource
def load_model(path):
    return YOLO(path)
model = load_model("modelo-chalecos/exp13/weights/best.pt")

# Placeholders para vídeo y estadísticas
video_placeholder = st.empty()
count_placeholder = st.metric("Último conteo", value="—")
history_chart = st.line_chart(pd.DataFrame({"detecciones": []}))

# Lista para guardar histórico de recuentos
counts = []

# Iniciar captura
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    st.error("❌ No se pudo abrir la cámara.")
    st.stop()

# Botón para detener la app
stop = st.sidebar.button("🔴 Detener captura")

while cap.isOpened() and not stop:
    ret, frame = cap.read()
    if not ret:
        st.warning("⚠️ No se pudo leer el frame.")
        break

    # Detectar con YOLO
    results = model.predict(source=frame, conf=conf_thres, imgsz=imgsz, stream=True)

    # Tomar solo el primer resultado (si usas stream=True siempre hay uno)
    r = next(results)
    annotated = r.plot()  # frame con cajas y etiquetas

    # Mostrar vídeo
    video_placeholder.image(
        cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB),
        channels="RGB",
        use_column_width=True,
    )

    # Estadísticas: número de detecciones en este frame
    n = len(r.boxes)
    count_placeholder.metric("Objetos detectados", n)
    counts.append({"timestamp": datetime.now(), "detecciones": n})

    # Actualizar gráfico con histórico
    df = pd.DataFrame(counts).set_index("timestamp")
    history_chart.add_rows(df.tail(1))

# Liberar recursos
cap.release()
