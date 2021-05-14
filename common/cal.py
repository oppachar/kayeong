from face_detection import *
from features_front import *
from features_side import *
from pytorch_face import num






############## 헤어스타일 추천
'''얼굴형 50
상중하안부 길이 20
옆광대 20
앞광대 10'''

# 얼굴형 받아오기
class_names = ["각진형", "계란형 ", "둥근형", "마름모형", "하트형"]

print(num)
print(class_names[num])

if (upper_ratio == center_ratio or upper_ratio == lower_ratio):
    ratio = 0 # 1:1:1

elif (upper_ratio > center_ratio and upper_ratio > lower_ratio):
    ratio = 1 # 상안부 길 때
elif (center_ratio > lower_ratio and center_ratio > upper_ratio):
    ratio = 2 # 중안부 길 때
elif (lower_ratio > upper_ratio and lower_ratio > center_ratio):
    ratio = 3 # 하안부 길 때



