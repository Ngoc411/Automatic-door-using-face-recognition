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
