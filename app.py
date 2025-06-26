from flask import Flask, render_template, Response, jsonify
from ultralytics import YOLO
import cv2
from datetime import datetime

app = Flask(__name__)
model = YOLO("modelo-chalecos/exp13/weights/best.pt")

# Variables globales
counts = []
last_count = 0

# Captura de video
cap = cv2.VideoCapture(0)

def generate_frames():
    global last_count, counts
    while True:
        success, frame = cap.read()
        if not success:
            break

        results = model.predict(source=frame, conf=0.5, imgsz=640, stream=True)
        r = next(results)
        annotated = r.plot()

        # Calcular confianza promedio
        confidences = [float(b.conf) for b in r.boxes] if r.boxes else [0]
        avg_conf = sum(confidences) / len(confidences) * 100 if confidences else 0

        last_count = len(r.boxes)
        counts.append({
            "timestamp": datetime.now().strftime('%H:%M:%S'),
            "detecciones": last_count,
            "confianza": round(avg_conf, 2)
        })

        ret, buffer = cv2.imencode('.jpg', annotated)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/stats')
def stats():
    return jsonify({
        "count": last_count,
        "history": counts[-30:]
    })

if __name__ == '__main__':
    app.run(debug=True)
