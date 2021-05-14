import dlib
import cv2
import numpy as np
from face_detection import image
from face_detection import ALL, RIGHT_EYEBROW, LEFT_EYEBROW, RIGHT_EYE, LEFT_EYE, NOSE, MOUTH_INNER, MOUTH_OUTLINE, JAWLINE
from face_detection import list_points, center, low


from FaceMeshBasics import cheekbone

print("468", cheekbone)

m = (cheekbone[3][2]- cheekbone[1][2])/(cheekbone[3][1]- cheekbone[1][1]) # 123번-192번 기울기

print("기울기" ,m)

if (m <= 3.7) :
    print("앞광대 O")
else :
    print("앞광대 X")


#cv2.imshow("result", image)
#cv2.imshow("8", image2)
cv2.waitKey(0)
cv2.destroyAllWindows()

