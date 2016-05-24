import os, time, datetime, json

import RPi.GPIO as GPIO
import picamera, dht11
import boto

print 'init dht11'
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
instance = dht11.DHT11(pin=14)

print 'get dht11 reading'
dht11_data = ''
result = instance.read()
if result.is_valid():
    dht11_data = {
        'Temperature': result.temperature,
        'Humidity': result.humidity
    }
    dht11_data = json.dumps(dht11_data)

print 'take picture'
file_name = str(time.time()).split('.')[0] + '.jpg'
with picamera.PiCamera() as camera:
    camera.resolution = (2592, 1944)
    camera.exif_tags['EXIF.UserComment'] = dht11_data
    camera.start_preview()
    time.sleep(2)
    camera.capture(file_name)

print 'upload image to s3'
client = boto.s3.connect_to_region(
    'eu-west-1',
    aws_access_key_id=os.environ["S3_KEY"],
    aws_secret_access_key=os.environ["S3_SECRET"]
)
bucket = client.get_bucket(os.environ["S3_BUCKET"])
key = bucket.new_key(file_name)
key.set_contents_from_filename(file_name)
key.make_public()
