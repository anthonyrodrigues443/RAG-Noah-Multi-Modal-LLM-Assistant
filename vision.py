import cvzone
from ultralytics import YOLO
import os
import cv2
from cvzone.HandTrackingModule import HandDetector
import time
import concurrent.futures

def setup_cam():
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    return cap

def object_detection(cap):
    model = YOLO('yolov9e.pt')
    print('this much done')
    class_names = list(model.names.values())
    detections = []

    first_frame = True
    stime = 0
    while True:
        success, img = cap.read()
        if not success:
            break

        results = model.predict(img, stream=True)
        for r in results:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                w, h = x2 - x1, y2 - y1
                cvzone.cornerRect(img, (x1, y1, w, h))

                # Confidence
                conf = float(box.conf[0])

                # Class Labels
                cls = int(box.cls[0])
                class_name = class_names[cls]

                # Add detection to list
                detection = {
                    "class_name": class_name,
                    "confidence": conf,
                    "bounding_box": [x1, y1, x2, y2]
                }
                detections.append(detection)

                # Display class name
                cvzone.putTextRect(img, f'{class_name} {conf:.2f}', (max(0, x1), max(35, y1)), scale=1, thickness=1)

        # Display the frame
        
        cv2.imshow('Obj_det', img)

        if first_frame:
            stime = time.time()
            first_frame=False
        
        if time.time() - stime > 5:
            break
        
        key = cv2.waitKey(1)
        if key == 32:
            break

    objects_detected = ''
    for detection in detections:
        objects_detected = detection['class_name'] +', '
    if objects_detected == '':
        objects_detected = 'None'
    cv2.destroyAllWindows()
    summary = 'Objects detected : ' + objects_detected
    return summary

def hand_tracking(cap):
    detector = HandDetector(detectionCon=0.9, maxHands=2)

    frame_num = 0
    left_hand_frames = []
    right_hand_frames = []
    types_of_hands_seen = set()
    stime = time.time()
    while True:
        captures, img = cap.read()
        hands, img = detector.findHands(img)
        cv2.imshow('Hand_trk', img)
        frame_num += 1

        if hands:
            for hand in hands:
                hand_type = hand['type'].lower()
                if hand_type == 'left':
                    left_hand_frames.append(frame_num)
                    if len(left_hand_frames) >= 5 and left_hand_frames[-3] == frame_num - 2:
                        types_of_hands_seen.add('left')
                elif hand_type == 'right':
                    right_hand_frames.append(frame_num)
                    if len(right_hand_frames) >= 5 and right_hand_frames[-3] == frame_num - 2:
                        types_of_hands_seen.add('right')
        if time.time() - stime > 5:
            break

        key = cv2.waitKey(1)
        if key == 32:
            break
    types_of_hands_seen = list(types_of_hands_seen)
    hands_detected = "No hand detected"
    if len(types_of_hands_seen) == 2:
        hands_detected = 'right , left'
    elif len(types_of_hands_seen) == 1:
        if types_of_hands_seen[0] == 'right':
            hands_detected = 'right'
        else :
            hands_detected = 'left'

    cv2.destroyAllWindows()

    summary = f"Total hands detected: {len(types_of_hands_seen)}\nDetected hand types: {hands_detected}"
    return summary

def run_concurrently(captures):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_obj_det = executor.submit(object_detection, captures)
        future_hand_trk = executor.submit(hand_tracking, captures)

        obj_det_res = future_obj_det.result()
        hand_trk_res = future_hand_trk.result()

        return obj_det_res, hand_trk_res
    
