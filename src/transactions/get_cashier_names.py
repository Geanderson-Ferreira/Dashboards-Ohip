import requests
from os import environ
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

def get_user_names(token, hotel):

    url = f"{environ['APIGW_URL']}/fof/config/v1/cashierDetails/cashiers?limit=4000"

    payload = {}
    headers = {
    'x-app-key': environ['APP_KEY'],
    'x-hotelid': hotel,
    'Authorization': f'Bearer {token}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.status_code == 200:
        dados = {item['cashierId'] : item['name'] for item in response.json()['cashiers']}

        return {
            'cahierId': dados.keys(),
            'cashierName': dados.values()
        }
    else:
        st.error(f"{response.text} on get_user_names")
        return False