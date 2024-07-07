import cvzone
from ultralytics import YOLO
import os
import cv2
from cvzone.HandTrackingModule import HandDetector
import time
import streamlit as st
import concurrent.futures
import warnings
from collections import Counter

warnings.filterwarnings('ignore')

def object_detection(cap):
    frame_placeholder = st.empty()
    model = YOLO('yolov10n.pt')
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
        
        rgb_frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        frame_placeholder.image(rgb_frame)

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
    frame_placeholder.empty()

    return summary

def hand_tracking(cap):
    frame_placeholder = st.empty()
    detector = HandDetector(detectionCon=0.9, maxHands=2)
    frame_num = 0
    left_hand_frames = []
    left_hand_fingers = []
    right_hand_frames = []
    right_hand_fingers = []
    types_of_hands_seen = set()
    finger_names = ['thumb', 'index finger', 'middle finger', 'ring finger',
                    'pinky finger']
    stime = time.time()
    while True:
        captures, img = cap.read()
        hands, img = detector.findHands(img)
        rgb_frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        frame_placeholder.image(rgb_frame)
        frame_num += 1

        if hands:
            for hand in hands:
                fingers_up = detector.fingersUp(hand)
                hand_type = hand['type'].lower()
                if hand_type == 'left':
                    left_hand_fingers.append(fingers_up)
                    left_hand_frames.append(frame_num)
                    if len(left_hand_frames) >= 5 and left_hand_frames[-3] == (frame_num - 2) :
                        types_of_hands_seen.add('left')
                        
                elif hand_type == 'right':
                    right_hand_fingers.append(fingers_up)
                    right_hand_frames.append(frame_num)
                    if len(right_hand_frames) >= 5 and right_hand_frames[-3] == (frame_num - 2) :
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

    #right-fingers-up, left-fingers-up
    rfu_tuples, lfu_tuples = [tuple(inner_list) for inner_list in right_hand_fingers], [tuple(inner_list) for inner_list in left_hand_fingers] 
    rfu, lfu = Counter(rfu_tuples), Counter(lfu_tuples)
    print(len(rfu), len(lfu))
    if len(rfu) == 0 or 'right' not in types_of_hands_seen:
        rfu = [0, 0, 0, 0, 0]
    else :
        rfu = list(rfu.most_common(1)[0][0])
    if len(lfu) == 0 or 'left' not in types_of_hands_seen:
        lfu = [0, 0, 0, 0, 0]
    else :
        lfu = list(lfu.most_common(1)[0][0])

    #right-finger-names, left-finger-names    
    rfn, lfn = '',''
    for i,j,k in zip(rfu,lfu,finger_names):
        if i == 1:
            rfn = rfn + k + ', ' 
        else : 
            pass
        if j == 1:
            lfn = lfn + k + ', ' 
        else : 
            pass
 
    
    summary = f"""Total hands detected: {len(types_of_hands_seen)}\n
Detected hand types: {hands_detected}\n
fingers up (left hand) : {sum(lfu)} ({lfn})\n
fingers up (right hand) : {sum(rfu)} ({rfn})
Total fingers detected : {sum(lfu) + sum(rfu)}
"""
    frame_placeholder.empty()
    return summary

def run_concurrently(captures):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_obj_det = executor.submit(object_detection, captures)
        future_hand_trk = executor.submit(hand_tracking, captures)

        obj_det_res = future_obj_det.result()
        hand_trk_res = future_hand_trk.result()

        return obj_det_res, hand_trk_res
