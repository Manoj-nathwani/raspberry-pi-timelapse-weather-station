import os, time, datetime

import RPi.GPIO as GPIO
import picamera, dht11
import boto

print 'initialising dht11'
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
instance = dht11.DHT11(pin=14)

print 'getting dht11 reading'
Temperature, Humidity = ''
result = instance.read()
if result.is_valid():
    temperature = result.temperature,
    humidity = result.humidity

print 'taking picture'
file_name = str(time.time()).split('.')[0] + '.jpg'
with picamera.PiCamera() as camera:
    camera.resolution = (2592, 1944)
    camera.start_preview()
    time.sleep(2)
    camera.capture(file_name)

print 'uploading image to s3'
connection = boto.s3.connect_to_region(
    'eu-west-1',
    aws_access_key_id=os.environ['S3_KEY'],
    aws_secret_access_key=os.environ['S3_SECRET']
)
bucket = connection.get_bucket(os.environ['S3_BUCKET'])
key = bucket.new_key(file_name)
key.set_metadata('temperature', temperature)
key.set_metadata('humidity', humidity)
key.set_contents_from_filename(file_name)
key.make_public()
