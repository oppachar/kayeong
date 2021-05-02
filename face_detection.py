import dlib
import cv2
import numpy as np

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

image = cv2.imread("10.jpg")
#image2 = cv2.imread("8.jpg")

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
rects = detector(gray, 1)

for face in rects:
    shape = predictor(gray, face)

    list_points = []
    for p in shape.parts():
        list_points.append([p.x, p.y])

    list_points = np.array(list_points)

    '''for i, pt in enumerate(list_points[JAWLINE]):
        pt_pos = (pt[0], pt[1])
        if (i == 3 or i == 4 or i == 5):
            cv2.circle(image, pt_pos, 2, (0, 255, 0), -1)
            print(i, pt_pos)'''

    for i, pt in enumerate(list_points[ALL]):
        pt_pos = (pt[0], pt[1])
        cv2.circle(image, pt_pos, 2, (0, 255, 0), -1)


x = (list_points[JAWLINE][3]-list_points[JAWLINE][4])[0]
y = (list_points[JAWLINE][3]-list_points[JAWLINE][4])[1]
print(y/x) # 기울기 사각턱이면 점간의 기울기가 더 클 것으로 예상
'''print((list_points[NOSE][6]-list_points[RIGHT_EYEBROW][4])[1],": 중안부 좌표 길이") # 중안부 좌표 길이
print((list_points[JAWLINE][8]-list_points[NOSE][6])[1],": 하안부 좌표 길이") # 하안부 좌표 길이'''

cv2.imshow("result", image)
#cv2.imshow("10", image2)



# gray = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
# rects = detector(gray, 1)

# for face in rects:
#     shape = predictor(gray, face)

#     list_points = []
#     for p in shape.parts():
#         list_points.append([p.x, p.y])

#     list_points = np.array(list_points)

#     '''for i, pt in enumerate(list_points[JAWLINE]):
#         pt_pos = (pt[0], pt[1])
#         #print(i, pt_pos)
#         if (i == 3 or i == 4 or i ==5):
#             cv2.circle(image2, pt_pos, 2, (0, 255, 0), -1)
#             print(i, pt_pos)'''

#     for i, pt in enumerate(list_points[ALL]):
#         pt_pos = (pt[0], pt[1])
#         cv2.circle(image2, pt_pos, 2, (0, 255, 0), -1)

# x = (list_points[JAWLINE][3]-list_points[JAWLINE][4])[0]
# y = (list_points[JAWLINE][3]-list_points[JAWLINE][4])[1]
# print(y/x)

'''print((list_points[NOSE][6]-list_points[RIGHT_EYEBROW][4])[1],": 중안부 좌표 길이") # 중안부 좌표 길이
print((list_points[JAWLINE][8]-list_points[NOSE][6])[1],": 하안부 좌표 길이") # 하안부 좌표 길이'''


################0502 추가

#이목구비 면적 구하기

lip_w = abs(list_points[MOUTH_OUTLINE][0]-list_points[MOUTH_OUTLINE][6])[0] #입술 가로
lip_h = abs(list_points[MOUTH_OUTLINE][4]-list_points[MOUTH_OUTLINE][8])[1] #입술 세로

print(lip_w,lip_h)
print("입 면적 : ", lip_w*lip_h)

nose_w = abs(list_points[NOSE][4]-list_points[NOSE][8])[0] #코 가로
nose_h = abs(list_points[NOSE][0]-list_points[NOSE][6])[1] #코 세로

print(nose_w, nose_h)
print("코 면적 : ", nose_w*nose_h)

leye_w = abs(list_points[LEFT_EYE][0]-list_points[LEFT_EYE][3])[0] #왼쪽 눈 가로
leye_h = abs(list_points[LEFT_EYE][1]-list_points[LEFT_EYE][5])[1] #왼쪽 눈 세로

print(leye_w, leye_h)
print("왼쪽 눈 면적 : ", leye_w*leye_h)

reye_w = abs(list_points[RIGHT_EYE][0]-list_points[RIGHT_EYE][3])[0] #오른쪽 눈 가로
reye_h = abs(list_points[RIGHT_EYE][1]-list_points[RIGHT_EYE][5])[1] #오른쪽 눈 세로

print(reye_w, reye_h)
print("오른쪽 눈 면적 : ", reye_w*reye_h)


'''#얼굴 전체 면적 구하기
face_w = (list_points[JAWLINE][1]-list_points[JAWLINE][15])[0] #얼굴 가로
face_h = (list_points[JAWLINE][8]-list_points[JAWLINE][15])[1] #얼굴 가로 (미완성)'''
#이마 끝 점이랑 턱 끝 좌표 비교해서 얼굴 세로 구하기



#콧볼 크기 판별
eyetoeye = abs(list_points[RIGHT_EYE][3]-list_points[LEFT_EYE][0])[0] #미간 거리

print("콧볼 크기 : ", nose_w)
print("미간거리 : ", eyetoeye)

if (nose_w + 10 > eyetoeye):
    print("콧볼이 큰 타입")
elif (nose_w + 10 < eyetoeye):
    print("콧볼이 작은 타입")
else:
    print("콧볼 비율 완벽")
#고정 픽셀값 정해놓으면 김태희사진(10) 기준으로 콧볼양끝값 조정하기


#cv2.imshow("Output", image)
#cv2.imshow("8", image2)
cv2.waitKey(0)
cv2.destroyAllWindows()

#print("Hello")