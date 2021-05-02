import dlib
import cv2
import numpy as np
from face_detection import image
from face_detection import ALL, RIGHT_EYEBROW, LEFT_EYEBROW, RIGHT_EYE, LEFT_EYE, NOSE, MOUTH_INNER, MOUTH_OUTLINE, JAWLINE
from face_detection import list_points, center, low
from hairline_detection import hair_line_point

#이목구비 면적 구하기

lip_w = abs(list_points[MOUTH_OUTLINE][0]-list_points[MOUTH_OUTLINE][6])[0] #입술 가로
lip_h = abs(list_points[MOUTH_OUTLINE][4]-list_points[MOUTH_OUTLINE][8])[1] #입술 세로

# print(lip_w, lip_h)
# print("입 면적 : ", lip_w*lip_h)

nose_w = abs(list_points[NOSE][4]-list_points[NOSE][8])[0] #코 가로
nose_h = abs(list_points[NOSE][0]-list_points[NOSE][6])[1] #코 세로

# print(nose_w, nose_h)
# print("코 면적 : ", nose_w*nose_h)

leye_w = abs(list_points[LEFT_EYE][0]-list_points[LEFT_EYE][3])[0] #왼쪽 눈 가로
leye_h = abs(list_points[LEFT_EYE][1]-list_points[LEFT_EYE][5])[1] #왼쪽 눈 세로

# print(leye_w, leye_h)
# print("왼쪽 눈 면적 : ", leye_w*leye_h)

reye_w = abs(list_points[RIGHT_EYE][0]-list_points[RIGHT_EYE][3])[0] #오른쪽 눈 가로
reye_h = abs(list_points[RIGHT_EYE][1]-list_points[RIGHT_EYE][5])[1] #오른쪽 눈 세로

# print(reye_w, reye_h)
# print("오른쪽 눈 면적 : ", reye_w*reye_h)


#얼굴 전체 면적 구하기
face_w = abs(list_points[JAWLINE][1]-list_points[JAWLINE][15])[0] #얼굴 가로
face_h = abs(list_points[JAWLINE][8]-hair_line_point)[1] #얼굴 세로

print("얼굴 가로 길이 : ", face_w)
print("얼굴 세로 길이 : ", face_h)

#콧볼 크기 판별
eyetoeye = abs(list_points[RIGHT_EYE][3]-list_points[LEFT_EYE][0])[0] #미간 거리

print("콧볼 크기 : ", nose_w)
print("미간거리 : ", eyetoeye)

if (nose_w > eyetoeye):
    print("콧볼이 큰 타입")
elif (nose_w < eyetoeye):
    print("콧볼이 작은 타입")
else:
    print("콧볼 비율 평균")
#고정 픽셀값 정해놓으면 김태희사진 기준으로 콧볼양끝값 조정하기..?



#눈 가로 크기 판별
print("눈 가로 비율 : ", abs(face_w/reye_w))

if (abs(face_w/reye_w) >= 5.5 and abs(face_w/reye_w) <= 5.6):
    print("눈 가로 길이 평균")
elif (abs(face_w/reye_w) > 5.6):
    print("눈 가로 길이가 작은 편")
elif (abs(face_w/reye_w) < 5.5):
    print("눈 가로 길이가 긴 편")


#눈 세로 크기 판별
print("눈 세로 비율 : ", abs(face_h/reye_h))

if (abs(face_h/reye_h) >= 22.6 and abs(face_h/reye_h) <= 25):
    print("눈 세로 길이가 평균")
elif (abs(face_h/reye_h) > 25):
    print("눈 세로 길이가 작은 편")
elif (abs(face_h/reye_h) < 22.6):
    print("눈 세로 길이가 큰 편")

cv2.imshow("result", image)
#cv2.imshow("8", image2)
cv2.waitKey(0)
cv2.destroyAllWindows()

