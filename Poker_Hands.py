from ultralytics import YOLO
import cv2
import cvzone
import math
import  PokerHandFunction



cap = cv2.VideoCapture(0) # for webcam


model = YOLO('PokerHand.pt')

classNames = ['10C', '10D', '10H', '10S',
              '2C', '2D', '2H', '2S',
              '3C', '3D', '3H', '3S',
              '4C', '4D', '4H', '4S',
              '5C', '5D', '5H', '5S',
              '6C', '6D', '6H', '6S',
              '7C', '7D', '7H', '7S',
              '8C', '8D', '8H', '8S',
              '9C', '9D', '9H', '9S',
              'AC', 'AD', 'AH', 'AS',
              'JC', 'JD', 'JH', 'JS',
              'KC', 'KD', 'KH', 'KS',
              'QC', 'QD', 'QH', 'QS'
              ]



while True:
    success, img = cap.read()
    results = model(img, stream=True)
    hand = []
    for r in results:
        boxes = r.boxes
        for box in boxes:
            # Bounding boxes
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            w, h = x2 - x1, y2 - y1
            cvzone.cornerRect(img, (x1, y1, w, h))

            # Confidence
            conf = math.ceil((box.conf[0]*100))/100


            # Class name
            cls = int(box.cls[0])

            cvzone.putTextRect(img, f'{classNames[cls]}  ', (max(0, x1), max(35, y1)), scale=1.0, thickness=1)

            if conf > 0.5:
                hand.append(classNames[cls])


    hand = list(set(hand))
    print(hand)
    if len(hand) == 5:
        results = PokerHandFunction.findPokerHand(hand)
        cvzone.putTextRect(img, f'Your Hand{results}  ', (300, 75), scale=2.0, thickness=4)
        print(results)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
