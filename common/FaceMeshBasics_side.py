import cv2
import mediapipe as mp
import numpy as np
import time
from face_detection import image_side

#cap = cv2.VideoCapture("Videos/3.mp4")
pTime = 0

#img = cv2.imread("7.jpg")

mpDraw = mp.solutions.drawing_utils
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh(max_num_faces=2)
drawSpec = mpDraw.DrawingSpec(thickness=1, circle_radius=2)

imgRGB = cv2.cvtColor(image_side, cv2.COLOR_BGR2RGB)
results = faceMesh.process(imgRGB)

cheekbone = []
jawline = []

if results.multi_face_landmarks:
     for faceLms in results.multi_face_landmarks:
       ''' mpDraw.draw_landmarks(img, faceLms, mpFaceMesh.FACE_CONNECTIONS,
                                drawSpec,drawSpec)'''


       for id,lm in enumerate(faceLms.landmark):
                #print(lm)
            ih, iw, ic = image_side.shape
            x,y = int(lm.x*iw), int(lm.y*ih)

            #cv2.circle(img, (x, y), 2, (0,255,0), -1)
            # if (id == 116 or id == 123 or id == 147 or id == 213 or id == 192 or id == 345 or id == 352 or id == 376 or id == 433 or id == 416): # 광대 index에만 점을 찍음
            #     #print(id,x,y)
            #     pt_pos2 = (x, y)
            #     cheekbone.append([id, pt_pos2])
            #
            #     cv2.circle(image, (x, y), 2, (0, 255, 0), -1)

            # if (id == 345 or id == 352 or id == 376 or id == 433 or id == 416):  # test
            #     # print(id,x,y)
            #     pt_pos2 = (x, y)
            #     cheekbone.append([id, pt_pos2])
            #
            #     cv2.circle(image, (x, y), 2, (0, 255, 0), -1)

            if (id == 116 or id == 123 or id == 147 or id == 192 or id == 213):  # test
                # print(id,x,y)
                pt_pos2 = (x, y)
                #cheekbone.append([id, pt_pos2])
                cheekbone.append([id, x, y])
                cv2.circle(image_side, (x, y), 2, (0, 255, 0), -1)

            '''if (id == 102 or id == 278):  # 콧볼
                print("콧볼", id, x, y)
                cv2.circle(image, (x, y), 2, (0, 255, 0), -1)
                newnose.append([x,y])
                #newnose_w = np.array([newnose_w])'''


            if (id == 8 or id == 168 or id == 197 or id == 5 or id == 1 or id == 2):  # 콧대 index에만 점을 찍음
                #print(id, x, y)
                cv2.circle(image_side, (x, y), 2, (0, 255, 0), -1)

            if (id == 17 or id == 18 or id == 200 or id == 199 or id == 175):  # 앞턱 index에만 점을 찍음
                #print(id, x, y)
                cv2.circle(image_side, (x, y), 2, (0, 255, 0), -1)

            if (id == 14 or id == 15 or id == 16 or id == 17 or id == 0 or id == 11 or id == 13):  # 입술 index에만 점을 찍음
                # print(id, x, y)
                cv2.circle(image_side, (x, y), 2, (0, 255, 0), -1)

            if (id == 152 or id == 377 or id == 400 or id == 378 or id == 379 or id == 365 or id == 397 or id == 288 or id == 361):  # 옆턱 index에만 점을 찍음
                # print(id, x, y)
                cv2.circle(image_side, (x, y), 2, (0, 255, 0), -1)
                jawline.append([id, x, y])



'''cTime = time.time()
fps = 1 / (cTime - pTime)
pTime = cTime'''
'''cv2.putText(img, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN,
            3, (255, 0, 0), 3)'''

#cv2.imshow("468", image_side)
cv2.waitKey(0)
cv2.destroyAllWindows()