import requests
import json
from os import environ
from dotenv import load_dotenv

load_dotenv()

def get_transaction_names(hotel, token):

    url = f"{environ['APIGW_URL']}/lov/v1/listOfValues/hotels/{hotel}/transactionCodes"

    payload = ""
    headers = {
    'Content-Type': 'application/json',
    'x-app-key': environ['APP_KEY'],
    'x-hotelid': hotel,
    'Authorization': f'Bearer {token}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.status_code == 200:

        dados = {item["code"]: item['name'] for item in response.json()['listOfValues']['items']}

        return {
            "codes": dados.keys(),
            "transactionCodeName": dados.values()
        }
    
    else:
        return False

