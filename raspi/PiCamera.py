import base64
import requests
import json

from picamera import PiCamera
from datetime import datetime, timedelta
from time import sleep

def wait():
    # Calculate the delay to the start of the next hour
    next_hour = (datetime.now() + timedelta(seconds=30))
    delay = (next_hour - datetime.now()).seconds
    sleep(delay)


camera = PiCamera()
camera.resolution = (3280, 2464)
camera.framerate=15
camera.iso=100
#Automatic gain control to settle
sleep(3)
#Now fix the values
camera.shutter_speed=camera.exposure_speed
camera.exposure_mode='off'
g=camera.awb_gains
camera.awb_mode='off'
camera.awb_gains=g
url = 'http://23.101.72.8:5000/api/uploadPI'
headers = {'Content-Type': 'application/json'}
url2 = 'http://23.101.72.8:5000/api/model'

for filename in camera.capture_continuous('img{timestamp:%Y-%m-%d-%H-%M-%S}.jpg',resize=(410,308)):
    print('Captured %s' % filename)
    with open(filename,'rb') as imagefile: slika64B=base64.b64encode(imagefile.read())
    myobj = {'slikaPI' : slika64B.decode('ascii')}
    model = requests.post(url2, data = json.dumps(myobj), headers=headers)
    print('Klasa:'+model.text)
    myobj2 = {'ID_voca': 1, 'slikaPI' : slika64B.decode('ascii'), 'KlasaModel' : int(model.text)}
    x = requests.post(url, data = json.dumps(myobj2), headers=headers)
    print(x.text)
    wait()