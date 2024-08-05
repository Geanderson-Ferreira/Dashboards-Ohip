import requests
import json
from os import environ
from dotenv import load_dotenv
from flask import flash
import pandas as pd
from flatten_json import flatten

load_dotenv()

def get_token():
    url = "http://api.atrio.it4f.com.br:44368/Auth/login"

    payload = json.dumps({
    "username": environ['USER_TCPOS'],
    "password": environ['PASSWORD_TCPOS']
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code == 200:
        return response.json()['token']
    else:
        flash("Erro ao obter token TCPOS")
        return False



def get_tcpos_transactions(date_from, date_to, rid, token):

    url = f"http://api.atrio.it4f.com.br:44368/Transactions?DateFrom={date_from}&DateTo={date_to}&StoreTarz={rid}"

    payload = ""
    headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {token}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.status_code == 200:
        return response.json()
    else:
        flash("Erro ao obter transações TCPOS.")
        return False

def get_df_pandas_tcpos_transactions(date_from, date_to, rid):

    f = get_tcpos_transactions(date_from, date_to, rid, get_token())
    if not f:
        flash("Erro ao Obter DataFrame TCPOS")
        return False
    
    transactions = [x['transactions'] for x in f]

    data = dict()
    for transaction in transactions:

        items = transaction[0]['items']

        for item in items:
            for k, v in transaction[0].items():
                if k != 'isDeleted':
                    try:
                        data[k].append(v)
                    except:
                        data[k] = list()
                        data[k].append(v)

            for ke, va in item.items():
                try:
                    data[ke].append(va)
                except:
                    data[ke] = list()
                    data[ke].append(va)

    return pd.DataFrame(data)
    


