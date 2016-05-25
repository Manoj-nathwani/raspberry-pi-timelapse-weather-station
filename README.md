# Raspberry Pi Timelapse Weather Station

- Takes a picture using the [Raspberry Pi camera module](https://www.raspberrypi.org/products/camera-module-v2/)
- Gets a temperature & humidity reading from a [DHT11 sensor](http://www.uugear.com/portfolio/dht11-humidity-temperature-sensor-module/)
- Uploads the images to [AWS S3](https://aws.amazon.com/s3/) along with the temperature & humidity data which is saved as [User-Defined Metadata](http://docs.aws.amazon.com/AmazonS3/latest/dev/UsingMetadata.html) on the uploaded file

# Setup
Set up your enviroment variables by editing your `/etc/environment` and adding:
```
export DHT11_PIN=14
export S3_KEY=xxxxxxxxxxxxxxxxxxxx
export S3_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
export S3_BUCKET=xxxxxxxxxxxxxxxxxxxx
```
Then simply add app.py as a cronjob
