import Adafruit_DHT
import time
import requests
import logging
import os

logging.basicConfig(level=os.environ.get('LOG_LEVEL', 'INFO'))

DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = None

try:
    DHT_PIN = int(os.environ.get('DHT_PIN'))
except Exception as e:
    logging.error('DHT_PIN is not set in the env or invalid DHT_PIN!', e)
    exit(1)

SERVICE_HTTP_URL=os.environ.get('SERVICE_HTTP_URL');

if not SERVICE_HTTP_URL:
    logging.error('SERVICE_HTTP_URL is not set in the env')
    exit(1)


while True:
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)

    if humidity is not None and temperature is not None:
        logging.info("Temp={0:0.1f}C Humidity={1:0.1f}%".format(temperature, humidity))
        response = ''
        try:
            response = requests.get(f'https://sls-cus-dev-pi-sensor.azurewebsites.net/api/temp?temp={temperature}')
        except Exception as e:
            logging.error(e)
        else:
            logging.info(f'Received response from cloud function: {response.text}')
    else:
        logging.warning("Sensor failure. Check wiring.");

    time.sleep(3);
