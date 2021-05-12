# import dlib
# import cv2
# import numpy as np
# import imutils
#
# detector = dlib.get_frontal_face_detector()
# predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
#
# ALL = list(range(0, 68))
# RIGHT_EYEBROW = list(range(17, 22))
# LEFT_EYEBROW = list(range(22, 27))
# RIGHT_EYE = list(range(36, 42))
# LEFT_EYE = list(range(42, 48))
# NOSE = list(range(27, 36))
# MOUTH_OUTLINE = list(range(48, 61))
# MOUTH_INNER = list(range(61, 68))
# JAWLINE = list(range(0, 17)) # index 1, 15 = 옆광대
#
# index = ALL
#
# image = cv2.imread("14.jpg")
#
# image = imutils.resize(image, height=500) # image 크기 조절
#
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# rects = detector(gray, 1)
#
# for face in rects:
#     shape = predictor(gray, face)
#
#     list_points = []
#     for p in shape.parts():
#         list_points.append([p.x, p.y])
#
#     list_points = np.array(list_points)
#
#     for i, pt in enumerate(list_points[ALL]):
#         pt_pos = (pt[0], pt[1])
#         cv2.circle(image, pt_pos, 2, (0, 255, 0), -1)
#
# x = (list_points[JAWLINE][3]-list_points[JAWLINE][4])[0]
# y = (list_points[JAWLINE][3]-list_points[JAWLINE][4])[1]
# #print(y/x) # 기울기 사각턱이면 점간의 기울기가 더 클 것으로 예상
#
# center = (list_points[NOSE][6]-list_points[RIGHT_EYEBROW][4])[1]
# low = (list_points[JAWLINE][8]-list_points[NOSE][6])[1]
#
#
# #cv2.imshow("Output", image)
# #cv2.imshow("8", image2)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
#
import dlib
import cv2
import numpy as np
import imutils

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

ALL = list(range(0, 68))
RIGHT_EYEBROW = list(range(17, 22))
LEFT_EYEBROW = list(range(22, 27))
RIGHT_EYE = list(range(36, 42))
LEFT_EYE = list(range(42, 48))
NOSE = list(range(27, 36))
MOUTH_OUTLINE = list(range(48, 61))
MOUTH_INNER = list(range(61, 68))
JAWLINE = list(range(0, 17)) # index 1, 15 = 옆광대

index = ALL

image = cv2.imread("before.jpg")

image = imutils.resize(image, height=500) # image 크기 조절

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
rects = detector(gray, 1)

for face in rects:
    shape = predictor(gray, face)

    list_points = []
    for p in shape.parts():
        list_points.append([p.x, p.y])

    list_points = np.array(list_points)

    for i, pt in enumerate(list_points[ALL]):
        pt_pos = (pt[0], pt[1])
        cv2.circle(image, pt_pos, 2, (0, 255, 0), -1)

    # for i, pt in enumerate(list_points[JAWLINE]):
    #     pt_pos = (pt[0], pt[1])
    #     if (i==1 or i==2 or i==3 or i==14 or i==15 or i==16):
    #         cv2.circle(image, pt_pos, 2, (0, 255, 0), -1)

p = (list_points[NOSE][0]+list_points[RIGHT_EYEBROW][4])/2 +1
center = (list_points[NOSE][6]-p)[1]
low = (list_points[JAWLINE][8]-list_points[NOSE][6])[1]

#cv2.imshow("Output", image)
cv2.waitKey(0)
cv2.destroyAllWindows()