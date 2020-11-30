import logging
import os
import azure.functions as func
from azure.cosmos import CosmosClient
from random_object_id import generate

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=os.environ.get('LOG_LEVEL', 'INFO'),
    datefmt='%Y-%m-%d %H:%M:%S')


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Access temperature/humidity
    try:
        temp = get_request_param(req, 'temp')
        hum = get_request_param(req, 'hum')
    except Exception as e:
        logging.error('Error getting temp and hum from request: ', e)
        return func.HttpResponse(
            f"Please pass temperature and humidity in the query string or in the request body. Error: {e}",
            status_code=400
        )

    logging.info(f'Received temperature {temp} and humidity {hum}')

    # Store in database
    try:
        save(temp, hum)
    except Exception as e:
        logging.error('Error storing into db: ', e)
        return func.HttpResponse(
            f"Error saving into db: {e}",
            status_code=500
        )

    logging.info(f'Successfully stored in DB')


def get_request_param(req, param_name) -> int:
    param = req.params.get(param_name)

    if not param:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            param = req_body.get(param_name)

    return int(param)


def save(temp, hum):
    url = os.environ.get('AZURE_COSMOS_URL')
    key = os.environ.get('AZURE_COSMOS_KEY')
    client = CosmosClient(url, credential=key)

    database_name = os.environ.get('AZURE_COSMOS_DATABASE_NAME')
    container_name = os.environ.get('AZURE_COSMOS_CONTAINER_NAME')

    database_client = client.get_database_client(database_name)
    container_client = database_client.get_container_client(container_name)

    container_client.upsert_item({
            'id': generate(),
            'temperature': temp,
            'humidity': hum
        }
    )
