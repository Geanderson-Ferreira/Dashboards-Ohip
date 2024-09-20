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
  
  response_data = list()
  hasMore = True
  offset=1
  while hasMore:
      # Requisição de reservas
      url = f"{environ['APIGW_URL']}/rsv/v1/hotels/{hotel}/reservations?limit=200&offset={offset}"
      
      headers = {
          'Content-Type': 'application/json',
          'x-hotelid': hotel,
          'x-app-key': environ['APP_KEY'],
          'Authorization': f'Bearer {token}'
      }

      response = requests.get(url, headers=headers, params=filtered_dict)
    #   st.write(response.url)

      if response.status_code != 200:
          hasMore = False
          # log.error(f"Erro ao obter reservas do hotel {hotel}")
          continue

      if response.json().get('reservations', {}).get('totalResults', 0) == 0:
          hasMore = False
          # log.info(f"Hotel {hotel} possui zero resultados.")
          continue
      
      response_data.extend(response.json()['reservations']['reservationInfo'])

      hasMore = response.json()['reservations']['hasMore']
      offset = response.json()['reservations']['offset']
  

  #
  response.json()['reservations']['reservationInfo'] = response_data
  return response_data