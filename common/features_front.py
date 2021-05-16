import dlib
import cv2
import numpy as np
from face_detection import *
# from face_detection import image
# from face_detection import ALL, RIGHT_EYEBROW, LEFT_EYEBROW, RIGHT_EYE, LEFT_EYE, NOSE, MOUTH_INNER, MOUTH_OUTLINE, JAWLINE
# from face_detection import list_points
from hairline_detection import hair_line_point, up, center, low
from FaceMeshBasics_front import newnose

# 상중하안부 비율의 기준 정하기
if (up < center):
    if (up < low):
        criteria = up
    else :
        criteria = low

elif (center < low):
    if (center < up):
        criteria = center
    else :
        criteria = up

elif (low < up):
    if (low < center):
        criteria = low
    else :
        criteria = center

# 상중하안부 비율
upper_ratio = round(abs(up/criteria), 1)
center_ratio = round(abs(center/criteria), 1)
lower_ratio = round(abs(low/criteria),1)
print(upper_ratio, center_ratio, lower_ratio)


#이목구비 면적 구하기

lip_w = abs(list_points[MOUTH_OUTLINE][0]-list_points[MOUTH_OUTLINE][6])[0] # 입술 가로
lip_h = abs(list_points[MOUTH_OUTLINE][4]-list_points[MOUTH_OUTLINE][8])[1] # 입술 세로

# print(lip_w, lip_h)
# print("입 면적 : ", lip_w*lip_h)

nose_w = abs(list_points[NOSE][4]-list_points[NOSE][8])[0] # 코 가로
nose_h = abs(list_points[NOSE][0]-list_points[NOSE][6])[1] # 코 세로

# print(nose_w, nose_h)
# print("코 면적 : ", nose_w*nose_h)

leye_w = abs(list_points[LEFT_EYE][0]-list_points[LEFT_EYE][3])[0] # 왼쪽 눈 가로
leye_h = abs(list_points[LEFT_EYE][1]-list_points[LEFT_EYE][5])[1] # 왼쪽 눈 세로

# print(leye_w, leye_h)
# print("왼쪽 눈 면적 : ", leye_w*leye_h)

reye_w = abs(list_points[RIGHT_EYE][0]-list_points[RIGHT_EYE][3])[0] # 오른쪽 눈 가로
reye_h = abs(list_points[RIGHT_EYE][1]-list_points[RIGHT_EYE][5])[1] # 오른쪽 눈 세로

# print(reye_w, reye_h)
# print("오른쪽 눈 면적 : ", reye_w * reye_h)


# 얼굴 전체 면적
face_w = abs(list_points[JAWLINE][1]-list_points[JAWLINE][15])[0] # 얼굴 가로
face_h = abs(list_points[JAWLINE][8]-hair_line_point)[1] # 얼굴 세로

print("얼굴 가로 길이 : ", face_w)
print("얼굴 세로 길이 : ", face_h)

# 콧볼 크기 판별
# eyetoeye = abs(list_points[RIGHT_EYE][3]-list_points[LEFT_EYE][0])[0] # 미간 거리
#
# print("콧볼 크기 : ", nose_w)
# print("미간거리 : ", eyetoeye)
#
# if (nose_w > eyetoeye):
#     print("콧볼이 큰 타입")
# elif (nose_w < eyetoeye):
#     print("콧볼이 작은 타입")
# else:
#     print("콧볼 비율 평균")

'''print("콧볼 비율 : ", abs(face_w/nose_w))

if (abs(face_w/nose_w) >= 5.5 and abs(face_w/nose_w) <= 6.8):
    print("콧볼 크기 평균")
elif (abs(face_w/nose_w) < 5.5):
    print("콧볼 큰 편")
elif (abs(face_w/nose_w) > 6.8):
    print("콧볼 작은 편")'''


# 콧볼 최종
#newnose_w = abs(newnose[0][0] - newnose[1][0])
#print(newnose_w)

#print("콧볼 비율 : ", abs(face_w/newnose_w)) # 136/36 = 3.777777

print("오른쪽 눈 앞꼬리 좌표", list_points[RIGHT_EYE][3][0])
print("오른쪽 콧볼 끝 좌표", newnose[0][0])

if (abs(list_points[RIGHT_EYE][3][0] - newnose[0][0]) <= 3):
    print("콧볼 크기는 평균입니다")
elif (newnose[0][0] - list_points[RIGHT_EYE][3][0] > -3):
    print("콧볼 크기는 평균보다 %.1f%% 큰 편입니다" %(abs(newnose[0][0] - list_points[RIGHT_EYE][3][0])/face_w)    )
elif (newnose[0][0] - list_points[RIGHT_EYE][3][0] > 3):
    print("콧볼 크기 %.1f%% 작은 편입니다" %(abs(newnose[0][0] - list_points[RIGHT_EYE][3][0])/face_w))

#눈 가로 크기 판별

ratio_eyew = abs(face_w/reye_w)
print("눈 가로 비율 : ", ratio_eyew)

if (ratio_eyew >= 5.5 and ratio_eyew <= 5.85): # 평균값 = 5.675
    print("눈 가로 길이는 평균")
elif (ratio_eyew < 5.5):
    print("눈 가로 길이 평균보다 %.1f%% 긴 편" %(abs(5.675-ratio_eyew)))
elif (ratio_eyew > 5.85):
    print("눈 가로 길이 평균보다 %.1f%% 짧은 편" %(abs(5.675-ratio_eyew)))


#눈 세로 크기 판별

ratio_eyeh = abs(face_h/reye_h)
print("눈 세로 비율 : ", ratio_eyeh)

if (ratio_eyeh >= 22.6 and ratio_eyeh <= 25): # 평균비 = 23.8
    print("눈 세로 길이 평균")
elif (ratio_eyeh < 22.6):
    print("눈 세로 길이 평균보다 %.1f%% 긴 편" %(abs(23.8-ratio_eyeh)))
elif (ratio_eyeh > 25):
    print("눈 세로 길이 평균보다 %.1f%% 짧은 편" %(abs(23.8-ratio_eyeh)))

# 꼬막눈 판별
'''
p1 = list_points[RIGHT_EYE][0]
p2 = list_points[RIGHT_EYE][1]
p3 = list_points[RIGHT_EYE][2]
p4 = list_points[RIGHT_EYE][3]
p5 = list_points[RIGHT_EYE][4]
p6 = list_points[RIGHT_EYE][5]
ear = (abs(p2-p6)+abs(p3-p5))/(2*(abs(p1-p4)))
#print("눈의 비율", ear[1])
if (ear[1] <= 2.5):
    print("꼬막눈 여부 : O")
else :
    print("꼬막눈 여부 : X")'''



# 옆광대 여부
flag = 0
x = (list_points[JAWLINE][1]-list_points[JAWLINE][2])[0]
y = (list_points[JAWLINE][1]-list_points[JAWLINE][2])[1]
#print(abs(y/x))
if (abs(y/x) >= 7.0): flag= 1

x = (list_points[JAWLINE][14]-list_points[JAWLINE][15])[0]
y = (list_points[JAWLINE][14]-list_points[JAWLINE][15])[1]
#print(abs(y/x))
if (abs(y/x) >= 7.0): flag= 1

if (flag == 1):
    cheek_front = 1

    print("옆광대 여부 : O")
else :
    cheek_front = 0

    print("옆광대 여부 : X")


cv2.imshow("front result", image_front)
#cv2.imshow("8", image2)
cv2.waitKey(0)
cv2.destroyAllWindows()

