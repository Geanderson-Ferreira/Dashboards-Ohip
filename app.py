"""
Os modulos importados estão no __init__.py de modules.
Habilitar estes modules no controller.py e coloca-los no .env.
"""

import streamlit as st
from src.auth.auth import authenticate_this
from os import environ
from dotenv import load_dotenv
from src.controller import level_of_access
from modules import *

load_dotenv()
modules = environ['MODULES'].split(',')

st.set_page_config(layout="wide")

def main():

    if not 'module' in st.session_state:

        for module in modules:
            globals()['ctn' + module] = st.empty()
            globals()['btn' + module] = globals()['ctn' + module].button(module)
        
        st.session_state['created_module_buttons'] = True

        for module in modules:
            if globals()['btn' + module]:
                st.session_state['module'] = module

    if 'module' in st.session_state:
        if st.session_state['created_module_buttons']:
            for module in modules:
                globals()['ctn' + module].empty()
            st.session_state['created_module_buttons'] = False

        authenticate_this(globals()[level_of_access[st.session_state['module']]])

if __name__ == "__main__":

    authenticate_this(main)