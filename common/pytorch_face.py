import torch
import cv2
import torchvision
from torchvision import datasets, models, transforms
from PIL import Image, ImageOps
import numpy as np
import matplotlib.pyplot as plt
import os
import torchvision.models as models
import torch.nn as nn
from face_detection import image_front


def imshow(input, title):
    # torch.Tensor를 numpy 객체로 변환
    input = input.numpy().transpose((1, 2, 0))
    # 이미지 정규화 해제하기
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])
    input = std * input + mean
    input = np.clip(input, 0, 1)
    # 이미지 출력




transforms_test = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

device = torch.device("cpu")


PATH = 'model_76.pt'

# 모델 초기화
model = torch.load(PATH, map_location=torch.device('cpu'))
# 모델 불러오기
#model.load_state_dict(torch.load('82.pt', map_location=device))
# 드롭아웃 및 배치 정규화를 평가 모드로 설정
model.eval()

'''# 이미지 불러오기

image = Image.open('./front/before.jpg')
#print(type(image))
image.show()
image = transforms_test(image).unsqueeze(0).to(device)    # tensor 형태로'''

image2 = Image.fromarray(image_front)
#print(type(image))
image2 = transforms_test(image2).unsqueeze(0).to(device)
cv2.imshow("Output!!!!!", image_front)


class_names = ["각진형", "계란형 ", "둥근형", "마름모형", "하트형"]

with torch.no_grad():
    outputs = model(image2)
    _, preds = torch.max(outputs, 1)
    num = preds[0].tolist()
    imshow(image2.cpu().data[0], title='prediction: ' + class_names[preds[0]])
    print("댕쉰의 얼굴 형!!!!!!!은 바로바로바로!!~!~!~!~!!~!~! 두구두구두~!!~! : ", class_names[preds[0]])
    print(preds[0])
