import time, datetime, json

import RPi.GPIO as GPIO
import picamera, dht11
import boto

# init dht11
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
instance = dht11.DHT11(pin=14)

# get dht11_data
dht11_data = ''
result = instance.read()
if result.is_valid():
    dht11_data = {
        'Temperature': result.temperature,
        'Humidity': result.humidity
    }
    dht11_data = json.dumps(dht11_data)

# take picture
with picamera.PiCamera() as camera:
    camera.resolution = (2592, 1944)
    camera.exif_tags['EXIF.UserComment'] = dht11_data
    camera.start_preview()
    time.sleep(2)
    camera.capture('image.jpg')

# upload image to s3
client = boto.connect_s3(os.environ["S3_KEY"], os.environ["S3_SECRET"])
bucket = client.get_bucket(os.environ["S3_BUCKET"])
key = bucket.new_key('image.jpg')
key.set_contents_from_filename(uploadfile)
key.make_public()
url = create_url(BUCKET, KEY)
print "Uploaded image to " + url
