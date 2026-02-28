from flask import Flask, render_template, Response, jsonify
import cv2
from ultralytics import YOLO
import cvzone
import os
from datetime import datetime

app = Flask(__name__)

# Global variables dashboard sync ke liye
current_count = 0
system_status = "Scanning"

# Folders Setup
INCIDENT_FOLDER = 'incidents'
if not os.path.exists(INCIDENT_FOLDER):
    os.makedirs(INCIDENT_FOLDER)

# AI Model Load
model = YOLO('best.pt') 

camera = cv2.VideoCapture(0)

def generate_frames():
    global current_count, system_status
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            results = model(frame, stream=True)
            temp_count = 0
            
            for r in results:
                boxes = r.boxes
                temp_count = len(boxes) # Live count update
                
                for box in boxes:
                    conf = float(box.conf[0])
                    if conf > 0.5:
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        cls = int(box.cls[0])
                        class_name = model.names[cls]

                        # Weapon detect hone par Danger setup
                        if class_name in ['pistol', 'knife']:
                            color = (0, 0, 255)
                            system_status = "CRITICAL"
                            # Screen par bada DANGER text
                            cv2.putText(frame, "!!! DANGER: WEAPON !!!", (50, 50), 
                                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                        else:
                            color = (255, 0, 0)
                            system_status = "Active"

                        cvzone.cornerRect(frame, (x1, y1, x2 - x1, y2 - y1), l=15, rt=2, colorR=color)
                        cvzone.putTextRect(frame, f'{class_name} {conf:.2f}', (x1, y1 - 10), 
                                         scale=1, thickness=1, colorR=color)

            current_count = temp_count # Global count update
            ret, buffer = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Dashboard Bridge: Ye route frontend ko data bhejega
@app.route('/get_status')
def get_status():
    global current_count, system_status
    return jsonify({
        "count": current_count,
        "status": system_status,
        "time": datetime.now().strftime("%H:%M:%S")
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)