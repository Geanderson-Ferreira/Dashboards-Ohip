import requests
import json
from os import environ
from dotenv import load_dotenv

load_dotenv()

def get_transactions(hotel, inicio, fim, token, limit):

    url = f"{environ['APIGW_URL']}/csh/v1/hotels/{hotel}/financialPostings?limit={limit}&startDate={inicio}&endDate={fim}"

    payload = ""
    headers = {
    'Content-Type': 'application/json',
    'x-hotelid': hotel,
    'x-app-key': environ['APP_KEY'],
    'Authorization': f'Bearer {token}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()

