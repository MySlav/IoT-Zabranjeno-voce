from picamera import PiCamera
from datetime import datetime, timedelta
from base64 import b64encode
from time import sleep
from json import dumps
from requests import post


def wait():
    next_image = (datetime.now() + timedelta(seconds=3600))
    delay = (next_image - datetime.now()).seconds
    sleep(delay)


# For setting particular ID of fruit
ID_voca = 1

# Intializing and setting camer
camera = PiCamera()
camera.resolution = (3280, 2464)
camera.framerate = 15
camera.iso = 100
# Automatic gain control to settle
sleep(3)
# Now fix the values
camera.shutter_speed = camera.exposure_speed
camera.exposure_mode = 'off'
g = camera.awb_gains
camera.awb_mode = 'off'
camera.awb_gains = g

# REST API routes
url = 'http://23.101.72.8:5000/api/uploadPI'
headers = {'Content-Type': 'application/json'}
url2 = 'http://23.101.72.8:5000/api/model'

for filename in camera.capture_continuous(
        'img{timestamp:%Y-%m-%d-%H-%M-%S}.jpg', resize=(410, 308)):
    print('Captured %s' % filename)
    with open(filename, 'rb') as imagefile:
        slika64B = b64encode(imagefile.read()).decode('ascii')
    myobj = {'slikaPI': slika64B}
    model = post(url2, data=dumps(myobj), headers=headers)
    print('Klasa:'+model.text)
    myobj2 = {'ID_voca': 1, 'slikaPI': slika64B, 'KlasaModel': int(model.text)}
    x = post(url, data=dumps(myobj2), headers=headers)
    print(x.text)
    wait()
