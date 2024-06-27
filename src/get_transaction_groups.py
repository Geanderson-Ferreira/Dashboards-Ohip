import requests
from os import environ
from dotenv import load_dotenv

load_dotenv()

def get_transaction_groups(hotel, token):

  url = f"{environ['APIGW_URL']}/fof/config/v1/transactionGroups?hotels=H5519"

  payload = {}
  headers = {
    'x-hotelid': hotel,
    'x-app-key': environ['APP_KEY'],
    'Authorization': f'Bearer {token}'
  }

  response = requests.request("GET", url, headers=headers, data=payload)

  if response.status_code == 200:
    return {item['description']: item['code'] for item in response.json()['transactionGroups']}
  else:
    return False
