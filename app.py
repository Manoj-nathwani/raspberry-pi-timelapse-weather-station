import time, datetime

import RPi.GPIO as GPIO
import picamera, dht11
import boto

import settings

print 'initialising dht11'
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
instance = dht11.DHT11(pin=14)

print 'getting dht11 reading'
result = instance.read()
if result.is_valid():
    temperature = result.temperature
    humidity = result.humidity
else:
    temperature = ''
    humidity = ''

print 'taking picture'
timestamp = time.time()).split('.')[0]
file_name = str(timestamp + '.jpg'
with picamera.PiCamera() as camera:
    camera.resolution = (2592, 1944)
    camera.start_preview()
    time.sleep(5)
    camera.capture(file_name)

print 'uploading image to s3'
connection = boto.s3.connect_to_region(
    'eu-west-1',
    aws_access_key_id=settings.AWS_KEY,
    aws_secret_access_key=settings.AWS_SECRET
)
bucket = connection.get_bucket(settings.AWS_S3_BUCKET)
key = bucket.new_key(file_name)
key.set_metadata('temperature', temperature)
key.set_metadata('humidity', humidity)
key.set_contents_from_filename(file_name)
key.make_public()
