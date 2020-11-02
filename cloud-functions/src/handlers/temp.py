import logging

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    temp = req.params.get('temp')
    if not temp:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            temp = req_body.get('temp')

    if temp:
        return func.HttpResponse(f"Temp received {temp}!")
    else:
        return func.HttpResponse(
             "Please pass a temp on the query string or in the request body",
             status_code=400
        )
