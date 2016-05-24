import time, datetime, json
import RPi.GPIO as GPIO
import picamera, dht11

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
instance = dht11.DHT11(pin=14)

result = instance.read()
if result.is_valid():
    dht11_data = {
        'Temperature': result.temperature,
        'Humidity': result.humidity
    }
    with picamera.PiCamera() as camera:
        camera.resolution = (2592, 1944)
        camera.exif_tags['EXIF.UserComment'] = json.dumps(dht11_data)
        camera.start_preview()
        time.sleep(2)
        camera.capture('image.jpg')
