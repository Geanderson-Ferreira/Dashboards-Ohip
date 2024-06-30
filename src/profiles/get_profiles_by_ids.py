import requests
from os import environ
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

def get_profiles_by_ids(hotel, token, ids_list: list):

    ids = {
        'profileIds': ids_list
    }

    url = f"{environ['APIGW_URL']}/crm/v1/profilesByIds?limit=500"

    payload = ""

    headers = {
    'x-hotelid': hotel,
    'x-app-key': environ['APP_KEY'],
    'Authorization': f'Bearer {token}'
    }

    response = requests.get(url, headers=headers, data=payload, params=ids)

    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"{response.text} on get_profiles_by_ids")
        return False