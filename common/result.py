from face_detection import *
from features_front import *
from features_side import *
from pytorch_face import num



############## 헤어스타일 추천

# 얼굴형 받아오기
class_names = ["각진형", "계란형 ", "둥근형", "마름모형", "하트형"]

#print("얼굴형 번호 : ", num)
#print("얼굴형 :" , class_names[num])
#num = 0 이면 각진형 ~ num = 4 면 하트형



# 상중하안부 비율

#print("상중하안부 비율 : ", upper_ratio, center_ratio, lower_ratio) # 상중하 각 각 비율 변수

if (upper_ratio == center_ratio or upper_ratio == lower_ratio):
    ratio = 0 # 1:1:1
elif (upper_ratio > center_ratio and upper_ratio > lower_ratio):
    ratio = 1 # 상안부 길 때
elif (center_ratio > lower_ratio and center_ratio > upper_ratio):
    ratio = 2 # 중안부 길 때
elif (lower_ratio > upper_ratio and lower_ratio > center_ratio):
    ratio = 3 # 하안부 길 때


# 옆광대 여부

# if(cheek_front == 0) :
#
# elif :

#cheek_front = 1 이면 옆광대 O
#cheek_front = 0 이면 옆광대 X


#앞광대 여부

#cheek_side = 1 이면 옆광대 O
#cheek_side = 0 이면 옆광대 X



