import requests
import json
import pandas as pd
from flatten_json import flatten
from os import environ
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

def get_reservations(hotel, token, filters: dict):

  filtered_dict = {key: value for key, value in filters.items() if value}

  itens_to_remove = list()
  
  for key, value in filtered_dict.items():
      if type(value) == list:
          if value[0] == "":
              itens_to_remove.append(key)
  
  for col in itens_to_remove:
      del filtered_dict[col]
  
  url = f"{environ['APIGW_URL']}/rsv/v1/hotels/{hotel}/reservations?limit=500"

  payload = ""
  headers = {
    'Content-Type': 'application/json',
    'x-hotelid': hotel,
    'x-app-key': environ['APP_KEY'],
    'Authorization': f'Bearer {token}'
  }

  response = requests.get(url, headers=headers, data=payload, params=filtered_dict)
  # st.write(response.url)  

  if response.status_code == 200:
    return response.json()
  