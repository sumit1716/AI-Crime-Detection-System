from ultralytics import YOLO
import cv2
import cvzone

# Model load karo (n = nano, fast chalega)
model = YOLO("yolov8n.pt") 

cap = cv2.VideoCapture(0) # 0 for webcam, ya video file path

while True:
    success, img = cap.read()
    results = model(img, stream=True)

    for r in results:
        boxes = r.boxes
        for box in boxes:
            # Confidence score
            conf = box.conf[0]
            # Class Name
            cls = int(box.cls[0])
            currentClass = model.names[cls]

            # Agar 'Person' ya 'Knife/Gun' detect ho (Custom model ke baad)
            if conf > 0.5:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                
                cvzone.cornerRect(img, (x1, y1, x2 - x1, y2 - y1))
                cvzone.putTextRect(img, f'{currentClass} {conf:.2f}', (x1, y1 - 10))

    cv2.imshow("Crime Detection System", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()