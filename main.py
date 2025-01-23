import face_recognition as fr 
import cv2 
import cvzone
import numpy as np 
import mysql.connector as sql 
import io
from PIL import Image
import time
import os 

# kết nối với mysql và truy xuất dữ liệu 
host = '127.0.0.1'
user = 'root'
password = 'ngoc411@'
database = 'face_recognition'

# Kết nối đến PostgreSQL
db = sql.connect(host = host, user = user, password = password, database = database)
cursor = db.cursor()

query = "SELECT * FROM user_information"
cursor.execute(query)
information = cursor.fetchall()

# setup camera 
cap = cv2. VideoCapture(0)
cap.set(3, 640)  
cap.set(4, 480)  

# lấy dữ liệu ảnh khuôn mặt và mã hóa 
folderImages = 'images'
imagesList = os.listdir(folderImages)
id_picture = []
for i in imagesList:
    i = i.split('.')
    id_picture.append(i[0])
print(id_picture)

imgList = []
Ids = []
for image in imagesList:
    print(os.path.join(folderImages, image))
    imgList.append(cv2.imread(os.path.join(folderImages, image)))
    Ids.append(os.path.splitext(image)[0])

# print(imgList)

def findEncode(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = fr.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList, encode 

encodeList, encode = findEncode(imgList)
# print(encode)
# print(encodeList)
# print(Ids)

imgBackground = cv2.imread('backgrounds/background.png')

# lấy dữ liệu hình ảnh các chế độ hiển thị
folderModes = 'modes'
folderList = os.listdir(folderModes)
modesList = []
for mode in folderList:
    # print(os.path.join(folderModes, mode))
    modesList.append(cv2.imread(os.path.join(folderModes, mode)))

# lấy dữ liệu hình ảnh thông tin người dùng
folderInformation = 'information'
folderList2 = os.listdir(folderInformation)
informationList = []
for infor in folderList2:
    # print(os.path.join(folderModes, mode))
    informationList.append(cv2.imread(os.path.join(folderInformation, infor)))

match_index = -1
typeMode = 0
counter = 0
flag_print = True
screen = True 

while True:
    success, img = cap.read()

    imgs = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgs = cv2.cvtColor(imgs, cv2.COLOR_BGR2RGB)

    if flag_print == True:
        # print('no')
        typeMode = 0
        imgBackground[11:11 + 517, 740:740 + 320] = modesList[typeMode]

    flag_print = True

    faceCurFrame = fr.face_locations(imgs)
    encodeCurFrame = fr.face_encodings(imgs, faceCurFrame)

    imgBackground[11:11 + 517, 740:740 + 320] = modesList[typeMode]

    for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
        matches = fr.compare_faces(encodeList, encodeFace)
        faceDis = fr.face_distance(encodeList, encodeFace)
        print(matches)
        print(faceDis)

        matchIndex = np.argmin(faceDis)
        # match_index = matchIndex
        # print(matchIndex)

        y1, x2, y2, x1 = faceLoc
        y1, x2, y2, x1 = y1*4,x2*4, y2*4, x1*4
        bbox = x1, y1, x2 - x1, y2 - y1
        img = cvzone.cornerRect(img, bbox, rt = 0)

        for i, id_number in enumerate(id_picture):
            if i == matchIndex:
                for j, a in enumerate(information):
                    if id_number == str(a[1]):
                        match_index = j
                        print(information[j][:5])

        if matches[matchIndex]:
            flag_print = False
            # print('yes')
            screen = True
            if counter == 0:
                typeMode = 0
                counter = 1
            
    if screen == True:
        # content = True
        if counter != 0:
            if counter <15:
                imgBackground[11:11 + 517, 740:740 + 320] = informationList[match_index]
                # if content: 
                #     cv2.putText(modesList[typeMode], str(infor[matchIndex][1]), (90,276), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
                #     cv2.putText(modesList[typeMode], str(infor[matchIndex][2]), (90,328), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
                #     cv2.putText(modesList[typeMode], str(infor[matchIndex][3]), (90,380), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
                #     cv2.putText(modesList[typeMode], str(infor[matchIndex][4]), (90,434), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
                #     cv2.putText(modesList[typeMode], str(infor[matchIndex][5]), (90,486), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
                image = Image.open(io.BytesIO(information[match_index][5]))
                image_np = np.array(image)
                image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
                informationList[match_index][45:45+190, 65:65+190] = image_bgr
            if 15 <= counter < 35:
                typeMode = 1
                imgBackground[11:11 + 517, 740:740 + 320] = modesList[typeMode]
            if counter >= 35:
                screen = False
                counter = 0
            counter += 1
            # print(counter)

    imgBackground[32:32+480, 35:35+640] = img

    cv2.imshow('background', imgBackground)
    # cv2.imshow('ackground', infor_grap)
    # cv2.imshow('Face Attendance', img)cv2
    key = cv2.waitKey(1) & 0xFF
    if key == 27:
        break 

cap.release()
cv2.destroyAllWindows()