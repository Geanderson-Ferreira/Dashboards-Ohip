import streamlit as st
from src.auth.auth import authenticate_this
from modules.transactions import transactions_dash

from modules.reservations import reservations_dash

st.set_page_config(layout="wide")


if __name__ == "__main__":
    authenticate_this(transactions_dash)