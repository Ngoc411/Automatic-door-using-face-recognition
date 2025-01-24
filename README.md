# Automatic Door with Face Recognition Using Raspberry Pi 4

## Description
This project uses face recognition technology to automatically control a door, applied in attendance check, identity control. This system uses OpenCV and machine learning models for face detection and authentication. Based on the authentication result, it controls a servo motor to open or close the door.

## Features
### Real-time face recognition.
- This project identifies and authenticates faces in real-time, providing relevant user information and controlling a door mechanism as follows:
  
![image alt](https://github.com/Ngoc411/Automatic-door-using-face-recognition/blob/891d35c99282f7bc8749187392db03dfda564330/z4919849374500_f36938b58fbd2fd4013473915ef15f29.jpg)
### Automatic door control using a Raspberry Pi.
- Automatically open the door after recognizing the user

### Design

![image alt](https://github.com/Ngoc411/Automatic-door-using-face-recognition/blob/38c0c19ca5982e64a0bf5a5120d6e754e70f6826/z4919849715942_3f35fcb683f4dc47bdff133c2b6ae376.jpg)

![image alt](https://github.com/Ngoc411/Automatic-door-using-face-recognition/blob/a05deb3d986b3e59de2ed5228ae26c68ed26ae4d/z4919849733856_0116874d3ac357bbe35e945eb1a62d83.jpg)

## Installation
You can use this command to install Python packages directly in the system-wide environment using pip:
```bash
sudo rm /usr/lib/python3.11/EXTERNALLY-MANAGED
```

You can also create a virtual environment to install Python packages by following these steps:

Install venv library:
```bash
sudo apt update
sudo apt install python3-venv 
```

Create virtual environment:
```
python3 -m venv venv_name
```

Activate the virtual environment:
```
source venv_name/bin/activate
```

After activated the virtual environment, you can install python packages using: 
```
pip install <package_name>
```

Deactivate the virtual environment:
```
deactivate
```

In my case, i'm using a virtual environment to run these scripts. Recommend using virtual environment to prevent conflict with the system's root environment.

### Install requirements:
```
sudo apt update
```

```
pip install face_recognition
pip install opencv-python
```

```
pip install cvzone
pip install numpy
pip install pillow
pip install pigpio
```

## Raspberrypi config

![image alt](https://github.com/Ngoc411/Automatic-door-using-face-recognition/blob/dc2c3fad65a9fc3ffa8ede64422a5d958275852f/z4781413596106_7edf34a572cac53fedddd66abe3c6ddb.jpg)

Config servo right using GPIO 17, servo left using GPIO 27.
Supply a 5V power to servo motors.

## Usage

### Overview
The system processes user face data, encodes the faces for recognition, and uses this information to control the servo motors that operate the door. Below are the key steps:

---

### Loading User Face Data
```python
folderImages = 'images'
imagesList = os.listdir(folderImages)
id_picture = []

for i in imagesList:
    i = i.split('.')
    id_picture.append(i[0])
```

![image alt](https://github.com/Ngoc411/Automatic-door-using-face-recognition/blob/dcccf13e31b3784ec9a5678e7e859b598ef79bba/Screenshot%202025-01-24%20161023.png)

- The program scans the images folder for all image files.
- It extracts user IDs from the filenames (e.g., user1.jpg → user1).

```python
imgList = []
Ids = []

for image in imagesList:
    imgList.append(cv2.imread(os.path.join(folderImages, image)))
    Ids.append(os.path.splitext(image)[0])
```

- The images are loaded into the imgList array.
- User IDs are saved in the Ids list.

### Encoding faces

```python
def findEncode(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = fr.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList, encode

encodeList, encode = findEncode(imgList)
```

- This function converts images to RGB format and generates face encodings.
- The encodeList stores encoded data for each face, which will be compared to live video feed data.


### Loading Display Modes and User Information
```python
folderModes = 'modes'
folderList = os.listdir(folderModes)
modesList = []

for mode in folderList:
    modesList.append(cv2.imread(os.path.join(folderModes, mode)))
```

![image alt](https://github.com/Ngoc411/Automatic-door-using-face-recognition/blob/e89b7dd9e80c9276894cb59b9b55803f22c24c72/Screenshot%202025-01-24%20161125.png)

- Loads mode images (e.g., mode1.png, mode2.png) from the modes folder for display purposes.

```python
folderInformation = 'information'
folderList2 = os.listdir(folderInformation)
informationList = []

for infor in folderList2:
    informationList.append(cv2.imread(os.path.join(folderInformation, infor)))
```

![iamge alt](https://github.com/Ngoc411/Automatic-door-using-face-recognition/blob/301ab802f8225a4f7c7617c489929afac1dc80ab/Screenshot%202025-01-24%20161114.png)

- Loads user information images (e.g., user profiles) from the information folder.

```python
information_name = []
for i in folderList2:
    i = i.split('.')
    information_name.append(i[0])
```

- Extracts user information names from file names (e.g., user1.jpg → user1).

### Servo control function

```python
def control_servo_right(stop_servo_event):
```
```python
def control_servo_left(stop_servo_event):
```

- These functions control the servo motors for opening and closing the door based on the recognition result.

### Camera and Face Recognition Loop

```python
def active_camera():
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)  
    cap.set(4, 480)  

    while True:
        success, img = cap.read()
        imgs = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgs = cv2.cvtColor(imgs, cv2.COLOR_BGR2RGB)

        faceCurFrame = fr.face_locations(imgs)
        encodeCurFrame = fr.face_encodings(imgs, faceCurFrame)
```

- Initializes the camera and captures frames continuously.
- Converts the frames to RGB and detects faces in real-time.

```python
for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
    matches = fr.compare_faces(encodeList, encodeFace)
    faceDis = fr.face_distance(encodeList, encodeFace)
    matchIndex = np.argmin(faceDis)
```

- Compares detected faces with preloaded encodings.
- Finds the best match by calculating face distances.

### Starting Threads

```python
camera_thread = threading.Thread(target=active_camera)
camera_thread.start()
engine_thread_right.start()
engine_thread_left.start()

camera_thread.join()
engine_thread_right.join()
engine_thread_left.join()
```
