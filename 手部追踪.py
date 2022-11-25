# coding:UTF-8
import socket
import cv2
import mediapipe as mp

hands_datect = mp.solutions.hands.Hands(static_image_mode=False,  # 静态追踪，低于0.5置信度会再一次跟踪
                                        max_num_hands=2,  # 最多有几只手
                                        min_detection_confidence=0.9,  # 最小检测置信度
                                        min_tracking_confidence=0.9)  # 最小跟踪置信度

mpDraw = mp.solutions.drawing_utils

# 点的样式，线的样式 BGR，前一个参数是颜色，后一个是粗细
handLmStyle = mpDraw.DrawingSpec(color=(0, 255, 255), thickness=5)
handConStyle = mpDraw.DrawingSpec(color=(255, 255, 0), thickness=5)


def findHands(img, draw=True, flipType=True):
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands_datect.process(imgRGB)
    allHands = []
    h, w, c = img.shape
    if results.multi_hand_landmarks:
        for handType, handLms in zip(results.multi_handedness, results.multi_hand_landmarks):
            myHand = {}
            ## lmList
            mylmList = []
            xList = []
            yList = []
            for id, lm in enumerate(handLms.landmark):
                px, py, pz = int(lm.x * w), int(lm.y * h), int(lm.z * w)
                mylmList.append([px, py, pz])
                xList.append(px)
                yList.append(py)

            ## bbox
            xmin, xmax = min(xList), max(xList)
            ymin, ymax = min(yList), max(yList)
            boxW, boxH = xmax - xmin, ymax - ymin
            bbox = xmin, ymin, boxW, boxH
            cx, cy = bbox[0] + (bbox[2] // 2), \
                     bbox[1] + (bbox[3] // 2)

            myHand["lmList"] = mylmList
            myHand["bbox"] = bbox
            myHand["center"] = (cx, cy)

            if flipType:
                if handType.classification[0].label == "Right":
                    myHand["type"] = "Left"
                else:
                    myHand["type"] = "Right"
            else:
                myHand["type"] = handType.classification[0].label
            allHands.append(myHand)

            if draw:
                mpDraw.draw_landmarks(img, handLms,
                                      mp.solutions.hands.HAND_CONNECTIONS)
                cv2.rectangle(img, (bbox[0] - 20, bbox[1] - 20),
                              (bbox[0] + bbox[2] + 20, bbox[1] + bbox[3] + 20),
                              (255, 0, 255), 2)
                cv2.putText(img, myHand["type"], (bbox[0] - 30, bbox[1] - 30), cv2.FONT_HERSHEY_PLAIN,
                            2, (255, 0, 255), 2)
    if draw:
        return allHands, img
    else:
        return allHands


if __name__ == '__main__':
    # width, height = 400, 150
    width, height = 1280, 720
    cap = cv2.VideoCapture(0)
    cap.set(3, width)
    cap.set(4, height)
    data = []

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverAddressPort = ("127.0.0.1", 5052)

    while True:
        ret, img = cap.read()
        hands, img = findHands(img)
        data = []

        # # 地标值 - (x, y, z) * 21
        if hands:
            # # 让第一只手被发现
            hand1 = hands[0]
            # # 获取地标值建列表
            lmlist1 = hand1["lmList"]
            for lm in lmlist1:
                data.extend([lm[0], height - lm[1], lm[2]])

            sock.sendto(str.encode(str(data)), serverAddressPort)

        cv2.imshow("image", img)
        if cv2.waitKey(1) == ord(" "):
            break
