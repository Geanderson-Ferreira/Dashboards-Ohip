import requests
from os import environ
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

def get_profiles_by_ids(hotel, token, ids: list):


    limit = 190
    all_profiles = []

    for i in range(0, len(ids), limit):

        ids_to_request = ids[i:i + limit]

        url = f"{environ['APIGW_URL']}/crm/v1/profilesByIds"

        payload = {}
        headers = {
        'x-hotelid': hotel,
        'x-app-key': environ['APP_KEY'],
        'Authorization': f'Bearer {token}'
        }

        params = {
            "profileIds": ids_to_request,
        "fetchInstructions": ["Address", "Comment", "Communication", "Profile"]
        }

        response = requests.request("GET", url, headers=headers, data=payload, params=params)

        if response.status_code == 200:
            all_profiles.extend(response.json()['profiles'].get('profileInfo',[]))
        else:
            print(response.text)
            return False
        
    return all_profiles