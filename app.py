import streamlit as st
from src.auth.auth import authenticate_this
from modules.transactions import transactions_dash
from os import environ
from dotenv import load_dotenv
from modules.reservations import reservations_dash
from src.controller import level_of_access

load_dotenv()
modules = environ['MODULES'].split(',')

st.set_page_config(layout="wide")

if __name__ == "__main__":

    if not 'module' in st.session_state:

        for module in modules:
            globals()['btn' + module] = st.button(module)
        
        for module in modules:
            if globals()['btn' + module]:
                st.session_state['module'] = module
    
    if 'module' in st.session_state:
        authenticate_this(globals()[level_of_access[st.session_state['module']]])
    
    # authenticate_this(transactions_dash)