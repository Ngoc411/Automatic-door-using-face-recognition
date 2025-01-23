import cv2 
import cvzone
import face_recognition as fr 
import numpy as np 
import mysql.connector as sql 
from PIL import Image
import io
import os
import time
import pigpio
import threading

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
print(folderList2)
informationList = []
for infor in folderList2:
    # print(os.path.join(folderModes, mode))
    informationList.append(cv2.imread(os.path.join(folderInformation, infor)))
    
information_name = []
for i in folderList2:
    i = i.split('.')
    information_name.append(i[0])
print(information_name)

# Setup GPIO cho servo
servo_pin_right = 17
servo_pin_left = 27

# Khởi tạo đối tượng Pigpio
pi = pigpio.pi()

if not pi.connected:
    print("Không thể kết nối tới pigpio daemon.")
    exit()

# Đặt chế độ của GPIO là OUTPUT
pi.set_mode(servo_pin_right, pigpio.OUTPUT)
pi.set_mode(servo_pin_left, pigpio.OUTPUT)

# Khởi tạo biến dừng/khởi động luồng
stop_servo_event = threading.Event()
start_servo_event = threading.Event()

# Hàm điều khiển động cơ servo
def close_servo():
    a = 0
def control_servo_right(stop_servo_event):
    try:
        while not stop_servo_event.is_set():
            start_servo_event.wait()
            
            # Quay động cơ về góc 0
            pi.set_servo_pulsewidth(servo_pin_right, 1000)

            # Đợi cho đến khi Timer hoàn thành
            event_1 = threading.Event()
            timer = threading.Timer(8, lambda: event_1.set())
            timer.start()

            # Chờ sự kiện được đặt (đợi 8 giây)
            event_1.wait()

            # Quay động cơ về góc 90
            pi.set_servo_pulsewidth(servo_pin_right, 2000)

            # Đợi cho đến khi Timer hoàn thành
            event_2 = threading.Event()
            timer = threading.Timer(1, lambda: event_2.set())
            timer.start()

            # Chờ sự kiện được đặt (đợi 1 giây)
            event_2.wait()
            
            start_servo_event.clear()

    finally:
        # Đặt động cơ về trạng thái dừng
        pi.set_servo_pulsewidth(servo_pin_right, 0)
        
def control_servo_left(stop_servo_event):
    try:
        while not stop_servo_event.is_set():
            start_servo_event.wait()
            
            # Quay động cơ về góc 0
            pi.set_servo_pulsewidth(servo_pin_left, 2000)

            # Đợi cho đến khi Timer hoàn thành
            event_1 = threading.Event()
            timer = threading.Timer(8, lambda: event_1.set())
            timer.start()

            # Chờ sự kiện được đặt (đợi 8 giây)
            event_1.wait()

            # Quay động cơ về góc 180
            pi.set_servo_pulsewidth(servo_pin_left, 1000)

            # Đợi cho đến khi Timer hoàn thành
            event_2 = threading.Event()
            timer = threading.Timer(1, lambda: event_2.set())
            timer.start()

            # Chờ sự kiện được đặt (đợi 1 giây)
            event_2.wait()
            
            start_servo_event.clear()

    finally:
        # Đặt động cơ về trạng thái dừng
        pi.set_servo_pulsewidth(servo_pin_left, 0)

# Tạo một luồng mới để điều khiển động cơ servo
engine_thread_right = threading.Thread(target=control_servo_right, args=(stop_servo_event,))
engine_thread_left = threading.Thread(target=control_servo_left, args=(stop_servo_event,))

def active_camera():
    # setup camera 
    cap = cv2. VideoCapture(0)
    cap.set(3, 640)  
    cap.set(4, 480)  

    match_index = -1
    infor_number = -1
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
            infor_number = matchIndex
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
                start_servo_event.set()
                flag_print = False
                # print('yes')
                screen = True
                if counter == 0:
                    typeMode = 0
                    counter = 1
                
        if screen == True:            
            if counter != 0:
                if counter <15:

                    imgBackground[11:11 + 517, 740:740 + 320] = informationList[infor_number]
                   
                    image = Image.open(io.BytesIO(information[match_index][5]))
                    image_np = np.array(image)
                    image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
                    informationList[infor_number][45:45+190, 65:65+190] = image_bgr
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
 
        key = cv2.waitKey(1) & 0xFF
        if key == 27:
            break 

    cap.release()
    cv2.destroyAllWindows()

camera_thread = threading.Thread(target = active_camera)

camera_thread.start()
engine_thread_right.start()
engine_thread_left.start()

camera_thread.join()
engine_thread_right.join()
engine_thread_left.join()

