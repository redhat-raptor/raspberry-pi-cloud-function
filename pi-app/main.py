import Adafruit_DHT
import time
import requests
import logging
import os

from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=os.environ.get('LOG_LEVEL', 'INFO'),
    datefmt='%Y-%m-%d %H:%M:%S')

DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = None

try:
    DHT_PIN = int(os.environ.get('DHT_PIN'))
except Exception as e:
    logging.error('DHT_PIN is not set in the env or invalid DHT_PIN!')
    exit(1)

SERVICE_HTTP_URL = os.environ.get('SERVICE_HTTP_URL')

if not SERVICE_HTTP_URL:
    logging.error('SERVICE_HTTP_URL is not set in the env')
    exit(1)


while True:
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)

    if humidity is not None and temperature is not None:
        logging.info("Received Temp={0:0.1f}C Humidity={1:0.1f}% from sensor".format(temperature, humidity))
        response = ''
        try:
            response = requests.get(f'{SERVICE_HTTP_URL}?temp={temperature}&hum={humidity}')
            print(response.content)
        except Exception as e:
            logging.error(e)
        else:
            logging.info(f'Received response from cloud function: {response.text}')
            logging.info('HTTP API took %s seconds', response.elapsed.total_seconds())
            logging.info('HTTP API request size in bytes %s', len(response.content))
    else:
        logging.warning("Sensor failure. Check wiring.")

    time.sleep(3)
