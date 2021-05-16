import dlib
import cv2
import numpy as np
from face_detection import image_side
from face_detection import ALL, RIGHT_EYEBROW, LEFT_EYEBROW, RIGHT_EYE, LEFT_EYE, NOSE, MOUTH_INNER, MOUTH_OUTLINE, JAWLINE
from face_detection import list_points, center, low
from FaceMeshBasics_side import cheekbone

print("468", cheekbone)

m = (cheekbone[3][2]- cheekbone[1][2])/(cheekbone[3][1]- cheekbone[1][1]) # 123번-192번 기울기

print("기울기" ,m)

if (m <= 3.4) :
    print("앞광대 O")
    cheek_side = 1
else :
    print("앞광대 X")
    chhek_side = 0

# m2 = (jawline[7][2]- jawline[3][2])/(jawline[7][1]- jawline[3][1]) # 365번-397번 기울기
# m3 = (jawline[7][2]- jawline[1][2])/(jawline[7][1]- jawline[1][1]) # 397번-288번 기울기
# m4 = (jawline[1][2]- jawline[2][2])/(jawline[1][1]- jawline[2][1]) # 288번-361번 기울기
#
# print(jawline)
#
# print("세점 기울기", m2,m3,m4)


cv2.imshow("side result", image_side)
#cv2.imshow("8", image2)
cv2.waitKey(0)
cv2.destroyAllWindows()

