from ultralytics import YOLO
from sort import *
import cv2
import cvzone
import math

def Processor(filename,modelt):
    
    if(modelt=="yolov8n"):
        model = YOLO('../Yolo-Weights/yolov8n.pt')
        print(model)
    elif(modelt=="yolov8l"):
        model = YOLO('../Yolo-Weights/yolov8l.pt')
    elif(modelt=="ipdetect"):
        objectdetector = cv2.createBackgroundSubtractorMOG2(history=400,varThreshold=200)
    print(model)
    
    yoloclassNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
              "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
              "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
              "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
              "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
              "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush"
              ]
    
    tracker = Sort(max_age=20, min_hits=3, iou_threshold=0.3)
    
    video = cv2.VideoCapture(f'uploads/{filename}')
    
    length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    fid = 0
    frame_width = int(video.get(3))
    frame_height = int(video.get(4))
    size = (frame_width, frame_height)
    
    fresult = cv2.VideoWriter('output.avi', 
                         cv2.VideoWriter_fourcc(*'MJPG'),
                         10, size)
    while True:
        
        ret, frame = video.read()
        fid += 1
        if ret == True:
            if (modelt=="yolov8n" or modelt == "yolov8l") :
                pred = model(frame)
                detections = np.empty((0, 5))
                for r in pred:
                    boxes = r.boxes
                    for box in boxes:
                        x1, y1, x2, y2 = box.xyxy[0]
                        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                        w = x2 - x1
                        h = y2 - y1
            
                        conf = math.ceil((box.conf[0] * 100)) / 100
                        cls = int(box.cls[0])
                        currentClass = yoloclassNames[cls]
            
                        if currentClass == "car" or currentClass == "truck" or currentClass == "bus" \
                        or currentClass == "motorbike" and conf > 0.3:
                            #cvzone.cornerRect(frame, (x1, y1, w, h), l=9, rt=3)
                            currentArray = np.array([x1, y1, x2, y2, conf])
                            detections = np.vstack((detections, currentArray))

                resultsTracker = tracker.update(detections)
                
                for result in resultsTracker:
                    x1, y1, x2, y2, id = result
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    w = x2 - x1
                    h = y2 - y1
                    cvzone.cornerRect(frame, (x1, y1, w, h), l=9, rt=2, colorR=(255, 0, 255))
                    cvzone.putTextRect(frame, f' {int(id)}', (max(0, x1), max(35, y1)),
                                        scale=2, thickness=3, offset=10)
            
            elif(modelt=="ipdetect"):
                mask = objectdetector.apply(frame)
                contours,_ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                for cnt in contours:
                    area = cv2.contourArea(cnt)
                    x1, y1, w, h = cv2.boundingRect(cnt)
                    if (area > 1000 and w < 300 and h < 300):
                        cv2.drawContours(frame, [cnt], -1, (0,255,0),2)
                        
                        #cvzone.cornerRect(frame, (x1, y1, w, h), l=9, rt=2, colorR=(255, 0, 255))

            progress = ( fid / length ) * 100
            #print(progress)
            fresult.write(frame)
        
        else:
            break
    
    video.release()
    fresult.release()
    return 1