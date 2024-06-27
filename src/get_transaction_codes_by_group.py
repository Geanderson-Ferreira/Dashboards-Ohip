import requests
import json
from os import environ
from dotenv import load_dotenv

load_dotenv()

def get_codes_by_group(hotel, token, group):

  url = f"{environ['APIGW_URL']}/fof/config/v1/transactionCodes?hotels={hotel}&transactionGroupCodes={group}"

  payload = ""
  headers = {
    'Content-Type': 'application/json',
    'x-hotelid': hotel,
    'x-app-key': environ['APP_KEY'],
    'Authorization': f'Bearer {token}'
  }

  response = requests.request("GET", url, headers=headers, data=payload)

  if response.status_code == 200:
      return [item['code'] for item in response.json()['transactionCodes']]
  else:
      return False
  
def get_total_codes_by_groups(hotel, token, group_list):

  url = f"{environ['APIGW_URL']}/fof/config/v1/transactionCodes?hotels={hotel}&"
  for group in group_list:
    url += f"transactionGroupCodes={group}"

  payload = ""
  headers = {
    'Content-Type': 'application/json',
    'x-hotelid': hotel,
    'x-app-key': environ['APP_KEY'],
    'Authorization': f'Bearer {token}'
  }

  response = requests.request("GET", url, headers=headers, data=payload)

  if response.status_code == 200:
      return [item['code'] for item in response.json()['transactionCodes']]
  else:
      return False