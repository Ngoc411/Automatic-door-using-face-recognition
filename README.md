# Automatic Door with Face Recognition Using Raspberry Pi 4

## Description
This project uses face recognition technology to automatically control a door, enhancing security and convenience. It uses OpenCV and machine learning models to detect and authenticate faces.

## Features
### Real-time face recognition.
- Find face in screen and identify whether the face exist on the database
- Provide user information after recognized
  
![image alt](https://github.com/Ngoc411/Automatic-door-using-face-recognition/blob/891d35c99282f7bc8749187392db03dfda564330/z4919849374500_f36938b58fbd2fd4013473915ef15f29.jpg)
### Automatic door control using a Raspberry Pi.
- Automatically open the door after recognizing the user
- Database integration for authorized users.
- Email notifications for unauthorized access attempts.
### Design

![image alt](https://github.com/Ngoc411/Automatic-door-using-face-recognition/blob/38c0c19ca5982e64a0bf5a5120d6e754e70f6826/z4919849715942_3f35fcb683f4dc47bdff133c2b6ae376.jpg)

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
source venv_name/bin/active
```

After activated the virtual enviroment, you can install python packages using: 
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

## Code explain

### Loading User Face Data

```python
folderImages = 'images'
imagesList = os.listdir(folderImages)
id_picture = []

for i in imagesList:
    i = i.split('.')
    id_picture.append(i[0])
```
- The program loads all images from the images folder.
- It extracts user IDs from the image filenames (e.g., user1.jpg → user1).
```python
imgList = []
Ids = []

for image in imagesList:
    imgList.append(cv2.imread(os.path.join(folderImages, image)))
    Ids.append(os.path.splitext(image)[0])
```
- Loads each image in the images folder into imgList.
- Stores the image IDs (user names) in the Ids list.

###  Encoding Faces

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

- This function converts the loaded images to RGB format and generates face encodings.
- The encodeList will store the encodings for each user's face, which will later be used to compare against the live camera feed.

### Loading Display Modes and User Information

```python
folderModes = 'modes'
folderList = os.listdir(folderModes)
modesList = []

for mode in folderList:
    modesList.append(cv2.imread(os.path.join(folderModes, mode)))
```
- Loads all mode images from the modes folder (such as mode1.png, mode2.png, etc.).
```python
folderInformation = 'information'
folderList2 = os.listdir(folderInformation)
informationList = []

for infor in folderList2:
    informationList.append(cv2.imread(os.path.join(folderInformation, infor)))
```
- Loads all user information images from the information folder.
```python
information_name = []
for i in folderList2:
    i = i.split('.')
    information_name.append(i[0])
```
- Extracts user information filenames without extensions (e.g., user1.jpg → user1).

### Servo Control Functions
```python
def control_servo_right(stop_servo_event)
```
```python
def control_servo_left(stop_servo_event)
```
- These functions handle the servo motor movement by setting the pulse width.
- The motors rotate to specific angles (0°, 90°, and 180°) depending on the recognition result.

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
- Initializes the camera and continuously captures frames.
- Converts the captured frames to RGB format and detects faces using face_recognition.
```python
for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
    matches = fr.compare_faces(encodeList, encodeFace)
    faceDis = fr.face_distance(encodeList, encodeFace)
    matchIndex = np.argmin(faceDis)
```
- Compares the face encodings from the live feed against the preloaded encodings.
- Finds the closest match and calculates the face distance to identify the user.

### Start the threads
```python
camera_thread = threading.Thread(target = active_camera)
camera_thread.start()
engine_thread_right.start()
engine_thread_left.start()

camera_thread.join()
engine_thread_right.join()
engine_thread_left.join()
```
