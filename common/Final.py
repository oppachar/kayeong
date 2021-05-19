import imutils
import mediapipe as mp
from torchvision import datasets, models, transforms
import torch
from PIL import Image, ImageOps
import numpy as np
import dlib
import cv2
import numpy as np



# 얼굴형 분류해서 return 에는 얼굴형 인덱스가 출력될 것임!
def faceline(image_front, PATH):
    class_names = ["각진형", "계란형 ", "둥근형", "마름모형", "하트형"]

    transforms_test = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    device = torch.device("cpu")

    # 모델 초기화
    model = torch.load(PATH, map_location=torch.device('cpu'))
    # 모델 불러오기
    # 드롭아웃 및 배치 정규화를 평가 모드로 설정
    model.eval()
    # 이미지 불러오기
    image = transforms_test(image_front).unsqueeze(0).to(device)

    # 불러온 이미지를 얼굴형 분류 모델에 집어넣기
    with torch.no_grad():
        outputs = model(image)
        _, preds = torch.max(outputs, 1)
        num = preds[0].tolist()

    return num

def face_detection(image_front):
    gray = cv2.cvtColor(image_front, cv2.COLOR_BGR2GRAY)
    rects = detector(gray, 1)

    for face in rects:
        shape = predictor(gray, face)

        list_points = []
        for p in shape.parts():
            list_points.append([p.x, p.y])

        list_points = np.array(list_points)

        for i, pt in enumerate(list_points[ALL]):
            pt_pos = (pt[0], pt[1])
            cv2.circle(image_front, pt_pos, 2, (0, 255, 0), -1)

    p = (list_points[NOSE][0] + list_points[RIGHT_EYEBROW][4]) / 2 + 1
    center = (list_points[NOSE][6] - p)[1]
    low = (list_points[JAWLINE][8] - list_points[NOSE][6])[1]

    return  center, low, list_points

def hair_up (img1,list_points):
    cascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)

    def get_head_mask(img):
        """
        Get the mask of the head
        Cuting  BG
        :param img: source image
        :return:   Returns the mask with the cut out BG
        """
        mask = np.zeros(img.shape[:2], np.uint8)
        bgdModel = np.zeros((1, 65), np.float64)
        fgdModel = np.zeros((1, 65), np.float64)
        faces = faceCascade.detectMultiScale(img, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))  # Find faces
        if len(faces) != 0:
            x, y, w, h = faces[0]
            (x, y, w, h) = (x - 40, y - 100, w + 80, h + 200)
            rect1 = (x, y, w, h)
            cv2.grabCut(img1, mask, rect1, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)  # Crop BG around the head
        mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')  # Take the mask from BG

        return mask2



    def is_bold(pnt, hair_mask):
        """
        Check band or not
        :param pnt: The upper point of the head
        :param hair_mask: Mask with hair
        :return: True if Bald, else False
        """
        roi = hair_mask[pnt[1]:pnt[1] + 40, pnt[0] - 40:pnt[0] + 40]  # Select the rectangle under the top dot
        cnt = cv2.countNonZero(roi)  # Count the number of non-zero points in this rectangle
        # If the number of points is less than 25%, then we think that the head is bald
        if cnt < 800:
            # print("Bald human on phoro")
            return True
        else:
            # print("Not Bold")
            return False

    mask = get_head_mask(img1)

    cnts = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[1]
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    cnt = cnts[0]
    topmost = tuple(cnt[cnt[:, :, 1].argmin()][0])

    lower = np.array([0, 0, 100], dtype="uint8")  # Lower limit of skin color
    upper = np.array([255, 255, 255], dtype="uint8")  # Upper skin color limit
    converted = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)  # We translate into HSV color format
    skinMask = cv2.inRange(converted, lower, upper)  # Write a mask from places where the color is between the outside
    mask[skinMask == 255] = 0  # We remove the face mask from the mask of the head

    kernel1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    mask = cv2.dilate(mask, kernel1, iterations=1)
    i1 = cv2.bitwise_and(img1, img1, mask=mask)

    if is_bold(topmost, mask):
        cv2.rectangle(img1, topmost, topmost, (0, 0, 255), 5)
        print(topmost)



    # Otherwise we write that we are not bald and display the coordinates of the largest contour
    else:
        cnts = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[1]
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

        len_cnts = len(cnts[0])
        max_y = 0
        for c in range(len_cnts):
            point = (cnts[0][c][0][0], cnts[0][c][0][1])

            if (point[0] >= list_points[NOSE][0][0] - 5 and point[0] <= (list_points[NOSE][0][0]) + 5):

                if (max_y < point[1]):
                    max_y = point[1]

        hair_line_point = list_points[NOSE][0][0], max_y
        cv2.circle(img1, (list_points[NOSE][0][0], max_y), 2, (0, 255, 0), -1)

    up = (list_points[RIGHT_EYEBROW][4] - hair_line_point)[1]


    return up

def face_length_ratio (up, low, center):


    # 상중하안부 비율의 기준 정하기
    if (up < center):
        if (up < low):
            criteria = up
        else:
            criteria = low

    elif (center < low):
        if (center < up):
            criteria = center
        else:
            criteria = up

    elif (low < up):
        if (low < center):
            criteria = low
        else:
            criteria = center

    # 상중하안부 비율
    upper_ratio = round(abs(up / criteria), 1)
    center_ratio = round(abs(center / criteria), 1)
    lower_ratio = round(abs(low / criteria), 1)
    print(upper_ratio, center_ratio, lower_ratio)

    if (upper_ratio == center_ratio and upper_ratio == lower_ratio):
        ratio = 0  # 1:1:1
    elif (upper_ratio > center_ratio and upper_ratio > lower_ratio):
        ratio = 1  # 상안부 길 때
    elif (center_ratio > lower_ratio and center_ratio > upper_ratio):
        ratio = 2  # 중안부 길 때
    elif (lower_ratio > upper_ratio and lower_ratio > center_ratio):
        ratio = 3  # 하안부 길 때
    elif (upper_ratio < center_ratio and upper_ratio < lower_ratio):
        ratio = 4  # 상안부가 가장 짧을 때

    return ratio

# 옆광대 여부
def side_cheekbone_have(list_points):
    flag = 0
    x = (list_points[JAWLINE][1] - list_points[JAWLINE][2])[0]
    y = (list_points[JAWLINE][1] - list_points[JAWLINE][2])[1]
    print(abs(y/x))
    if (abs(y / x) >= 6.8): flag = 1

    ''' <광대 여부 있나 확인> 
    if (flag == 1):
        print("옆광대 여부 : O")
    else:
        print("옆광대 여부 : X")
    '''
    return flag

def nose_detection(list_points,image_front):

    pTime = 0

    mpDraw = mp.solutions.drawing_utils
    mpFaceMesh = mp.solutions.face_mesh
    faceMesh = mpFaceMesh.FaceMesh(max_num_faces=2)
    drawSpec = mpDraw.DrawingSpec(thickness=1, circle_radius=2)

    imgRGB = cv2.cvtColor(image_front, cv2.COLOR_BGR2RGB)
    results = faceMesh.process(imgRGB)

    nose = []

    if results.multi_face_landmarks:
        for faceLms in results.multi_face_landmarks:
            for id,lm in enumerate(faceLms.landmark):
                ih, iw, ic = image_front.shape
                x, y = int(lm.x * iw), int(lm.y * ih)

                if (id == 102 or id == 278):  # 콧볼
                    #print("콧볼", id, x, y)
                    cv2.circle(image_front, (x, y), 2, (0, 255, 0), -1)
                    nose.append([x, y])

    #print("ㅅㅂ")

    nose_w = abs(nose[0][0] - nose[1][0])
    ratio_nose = abs(face_w/nose_w)

    if (ratio_nose >= 3.5 and ratio_nose <= 4.0): #평균 3.7
        nose_result = 0
        nose_percent = 0
        #print("콧볼 크기는 평균입니다")
    elif (ratio_nose < 3.5):
        nose_result = 1
        nose_percent = abs(3.7 - ratio_nose)
        print("콧볼", ratio_nose)
        #print("콧볼 크기는 평균보다 %.1f%% 큰 편입니다" % (abs(nose[0][0] - list_points[RIGHT_EYE][3][0]) / face_w))
    elif (ratio_nose >= 4.0):
        nose_result = -1
        nose_percent = abs(3.7 - ratio_nose)
        print("콧볼", ratio_nose)

        #print("콧볼 크기 %.1f%% 작은 편입니다" % (abs(nose[0][0] - list_points[RIGHT_EYE][3][0]) / face_w))

    return nose_result, nose_percent

#눈 가로
def eyew_detection(list_points):
    reye_w = abs(list_points[RIGHT_EYE][0] - list_points[RIGHT_EYE][3])[0]  # 오른쪽 눈 가로

    ratio_eyew = abs(face_w / reye_w)

    if (ratio_eyew >= 5.5 and ratio_eyew <= 5.85):  # 평균값 = 5.675
        eyew_result = 0
        eyew_percent = 0
        #print("눈 가로 길이는 평균")
    elif (ratio_eyew < 5.5):
        eyew_result = 1
        eyew_percent = abs(5.675 - ratio_eyew)
        #print("눈 가로 길이 평균보다 %.1f%% 긴 편" % (abs(5.675 - ratio_eyew)))
    elif (ratio_eyew > 5.85):
        eyew_result = -1
        eyew_percent = abs(5.675 - ratio_eyew)
        #print("눈 가로 길이 평균보다 %.1f%% 짧은 편" % (abs(5.675 - ratio_eyew)))

    return eyew_result, eyew_percent

#눈 세로
def eyeh_detection(list_points):
    reye_h = abs(list_points[RIGHT_EYE][1] - list_points[RIGHT_EYE][5])[1]  # 오른쪽 눈 세로

    ratio_eyeh = abs(face_h / reye_h)

    if (ratio_eyeh >= 22.6 and ratio_eyeh <= 25):  # 평균비 = 23.8
        eyeh_result = 0
        eyeh_percent = 0
        #print("눈 세로 길이 평균")
    elif (ratio_eyeh < 22.6):
        eyeh_result = 1
        eyeh_percent = abs(23.8 - ratio_eyeh)
        #print("눈 세로 길이 평균보다 %.1f%% 긴 편" % (abs(23.8 - ratio_eyeh)))
    elif (ratio_eyeh > 25):
        eyeh_result = -1
        eyeh_percent = abs(23.8 - ratio_eyeh)
        #print("눈 세로 길이 평균보다 %.1f%% 짧은 편" % (abs(23.8 - ratio_eyeh)))

    return eyeh_result, eyeh_percent

#미간거리
def between_detection(list_points):
    eyetoeye = abs(list_points[RIGHT_EYE][3] - list_points[LEFT_EYE][0])[0]  # 미간 거리
    between_ratio = abs(face_w / eyetoeye)

    if (between_ratio >= 3.4 and between_ratio < 3.9):
        between_result = 0
        between_percent = 0
        #print("미간 평균 ", between_ratio)

    elif (between_ratio < 3.4):
        between_result = -1
        between_percent = abs(4.75 - between_ratio)
        #print("미간 짧은 편 ", between_ratio)
        #미간 긴 편
    elif (between_ratio > 3.9):
        between_result = 1
        between_percent = abs(4.75 - between_ratio)
        #print("미간 긴 편 ", between_ratio)

        #미간 짧은편

    return between_result, between_percent

def eyeshape_detection(list_points):

    p1 = list_points[RIGHT_EYE][0][1]
    p2 = list_points[RIGHT_EYE][1][1]
    p3 = list_points[RIGHT_EYE][2][1]
    p4 = list_points[RIGHT_EYE][3][1]
    p5 = list_points[RIGHT_EYE][4][1]
    p6 = list_points[RIGHT_EYE][5][1]

    if (p1 == p4):
        ear = 0
    else:
        ear = (abs(p2 - p6) + abs(p3 - p5)) / (2 * (abs(p1 - p4)))

    #print("눈의 비율", ear[1])
    if (ear <= 2.6):
        #print("꼬막눈 여부 : O")
        eyeshape_result = 1
    else:
        #print("꼬막눈 여부 : X")
        eyeshape_result = 0

    return eyeshape_result


# 앞광대 여부
def front_cheekbone_have(list_points,image_side):

    pTime = 0

    mpDraw = mp.solutions.drawing_utils
    mpFaceMesh = mp.solutions.face_mesh
    faceMesh = mpFaceMesh.FaceMesh(max_num_faces=2)
    drawSpec = mpDraw.DrawingSpec(thickness=1, circle_radius=2)

    imgRGB = cv2.cvtColor(image_side, cv2.COLOR_BGR2RGB)
    results = faceMesh.process(imgRGB)

    cheekbone = []
    if results.multi_face_landmarks:
        for faceLms in results.multi_face_landmarks:
            for id,lm in enumerate(faceLms.landmark):
                ih, iw, ic = image_side.shape
                x, y = int(lm.x * iw), int(lm.y * ih)
                if (id == 116 or id == 123 or id == 147 or id == 192 or id == 213):  # test
                    # print(id,x,y)
                    #pt_pos2 = (x, y)
                    # cheekbone.append([id, pt_pos2])
                    cheekbone.append([id, x, y])
                    cv2.circle(image_side, (x, y), 2, (0, 255, 0), -1)

    m = (cheekbone[3][2] - cheekbone[1][2]) / (cheekbone[3][1] - cheekbone[1][1])  # 123번-192번 기울기

    print("기울기", m)

    if (m <= 3.5):
        #print("앞광대 O")
        cheek_side = 1
    else:
        #print("앞광대 X")
        cheek_side = 0

    return cheek_side


# 이미지 읽어오기


image_front_origin = cv2.imread("./front/32.jpg")
image_side_origin = cv2.imread("./side/before.jpg")
image_faceline = Image.open("./front/32.jpg")

# 얼굴형 분류 모델의 위치 = PATH
PATH = 'model_76.pt'

image_front = imutils.resize(image_front_origin, height=500)  # image 크기 조절
image_side = imutils.resize(image_side_origin, height=500)  # image 크기 조절


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
JAWLINE = list(range(0, 17))  # index 1, 15 = 옆광대

index = ALL

faceline_index = faceline(image_faceline,PATH)

center, low, list_points = face_detection(image_front)

# 얼굴 비율 구할 때 필요한 맨 위 점 (헤어 라인 점 )
up = hair_up(image_front,list_points)

face_w = abs(list_points[JAWLINE][1]-list_points[JAWLINE][15])[0] # 얼굴 가로
face_h = abs(list_points[JAWLINE][8]-up)[1] # 얼굴 세로

''' <ratio 의미>
0 # 1:1:1
1 # 상안부 길 때
2 # 중안부 길 때
3 # 하안부 길 때
4 # 상안부 짧을 때

눈 세로
눈 가로
미간거리
앞광대
'''
ratio = face_length_ratio(up, center, low)

# 옆광대 유무 1: 있음 , 0: 없음
cheek_side = side_cheekbone_have(list_points)

# 앞광대 유무 1: 있음 , 0: 없음
cheek_front = front_cheekbone_have(list_points,image_side)

# 콧볼 0: 평균 , 1: 큼 , -1: 작음
nose_result, nose_percent = nose_detection(list_points,image_front)

# 눈 세로 0: 평균 , 1: 큼 , -1: 작음
eyeh_result, eyeh_percent = eyeh_detection(list_points)

# 눈 가로 0: 평균 , 1: 큼 , -1: 작음
eyew_result, eyew_percent = eyew_detection(list_points)

# 미간 0: 평균 , 1: 큼 , -1: 작음
between_result, between_percent = between_detection(list_points)

# 눈꼬리 1: 올라감 0: 올라가지않음
eyeshape_result = eyeshape_detection(list_points)

if(eyeshape_result == 1 and eyew_result == -1): #올라간 눈이면서 눈 짧으면
    shorteye_index = 1 # 꼬막눈 O
else:
    shorteye_index = 0 # 꼬막눈 X

print("얼굴형_인덱스", faceline_index) #"각진형", "계란형 ", "둥근형", "마름모형", "하트형"
print("얼굴 비", ratio)
print("얼굴 옆광대", cheek_side)
print("얼굴 앞광대", cheek_front)

print("콧볼", nose_result, nose_percent)
print("미간", between_result, between_percent)
print("눈 세로", eyeh_result, eyeh_percent)
print("눈 가로", eyew_result, eyew_percent)
print("올라간 눈", eyeshape_result)
print("꼬막눈", shorteye_index)

cv2.imshow("front result", image_front)
cv2.imshow("side result", image_side)

cv2.waitKey(0)
cv2.destroyAllWindows()
