# Automatic Door with Face Recognition Using Raspberry Pi 4

## Description
This project uses face recognition technology to automatically control a door, enhancing security and convenience. It uses OpenCV and machine learning models to detect and authenticate faces.

## Features
- Real-time face recognition.
- Automatic door control using a Raspberry Pi.
- Database integration for authorized users.
- Email notifications for unauthorized access attempts.

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

1. Install requirements:
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
