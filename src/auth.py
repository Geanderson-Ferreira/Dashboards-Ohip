import streamlit as st
import time
import requests
from os import environ
from dotenv import load_dotenv

load_dotenv()

def get_token(username, password):

    url = f"{environ['APIGW_URL']}/oauth/v1/tokens"

    payload = f'username={username}&password={password}&grant_type=password'
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'x-app-key': environ['APP_KEY'],
    'Authorization': f'Basic {environ['AUTHORIZATION']}'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code == 200:
        return response.json()
    else:
        return False

class Authenticate:
    def __init__(self):
        self.is_authenticated = False

    def check(self, username, password):
        checker = get_token(username, password)
        if checker != False:

            st.session_state['token'] = checker['access_token']
            self.is_authenticated = True 
            return True
        else:
            return False
        
def authenticate_this(function):

    auth = Authenticate()

    # Página de login
    if 'token' not in st.session_state:

        user_container = st.empty()
        pass_container = st.empty()
        btn_container = st.empty()
        alert_container = st.empty()

        username = user_container.text_input("Username")
        password = pass_container.text_input("Password", type="password")
        login_button = btn_container.button("Login")

        if login_button:
            auth.check(username, password)

    if auth.is_authenticated:
        alert_container.success("Login successful!")
        time.sleep(1)
        user_container.empty()
        pass_container.empty()
        btn_container.empty()
        alert_container.empty()
        function()

