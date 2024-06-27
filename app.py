import streamlit as st
from src.auth import Authenticate
import time
from src.get_transactions import get_transactions
from src.auth import get_token, authenticate_this
from src.get_transaction_codes import get_transaction_names
from src.get_cashier_names import get_user_names
from src.get_transaction_groups import get_transaction_groups
from src.get_transaction_codes_by_group import get_codes_by_group

import pandas as pd
import datetime

st.set_page_config(layout="wide")

hotel = 'H5519'
inicio = '2024-06-25'
fim = '2024-06-25'
limit = 3000
t = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsIng1dCI6IjFCZUYycEpFQWQtY3g2d3BnU3IyTkFZbkVtdyIsImtpZCI6Im1zLW9hdXRoa2V5In0.eyJzdWIiOiJpbnRlZ3JhY2FvX2dlYW5kZXJzb24iLCJpc3MiOiJ3d3cub3JhY2xlLmNvbSIsIm9yYWNsZS5vYXV0aC5zdmNfcF9uIjoiT0F1dGhTZXJ2aWNlUHJvZmlsZSIsImlhdCI6MTcxOTQ2MTY3NCwib3JhY2xlLm9hdXRoLnBybi5pZF90eXBlIjoiTERBUF9VSUQiLCJleHAiOjE3MTk0NjUyNzQsIm9yYWNsZS5vYXV0aC50a19jb250ZXh0IjoidXNlcl9hc3NlcnRpb24iLCJhdWQiOlsiaHR0cHM6Ly8qb3JhY2xlKi5jb20iLCJodHRwczovLyouaW50ICIsImh0dHBzOi8vKm9jcy5vYy10ZXN0LmNvbS8iXSwicHJuIjoiaW50ZWdyYWNhb19nZWFuZGVyc29uIiwianRpIjoiZDM0ZTRkYWMtYTU0OC00NGQyLTk5MTAtYmJlOWZjYjU4YTFjIiwib3JhY2xlLm9hdXRoLmNsaWVudF9vcmlnaW5faWQiOiJBQ0NPUkFUX0NsaWVudCIsInVzZXIudGVuYW50Lm5hbWUiOiJEZWZhdWx0RG9tYWluIiwib3JhY2xlLm9hdXRoLmlkX2RfaWQiOiIxMjM0NTY3OC0xMjM0LTEyMzQtMTIzNC0xMjM0NTY3ODkwMTIifQ.UpakQyyVS_u462Gd-f3LBpSLL-r93fSwuzVXbjggWqhvasXouh5164hyoppc2jGxnQWGrIoZlli1SKY9DaqeksDqiMTFNMyekAeVjo6DAKfBSMnd3JfLHnql3mOqDwVQJi0iuZhmDFaRvEqyZcgk-B3yoTUxxZkt2k53laRNDzFWzblrottFWcH8pSPS1fMWINGzWUIssj62j5vfL0WB5fwitf5Q8Gp8vhA70LikEqFr90rkV0VD_tkNoJm_TJouaNiYwxeqOReyoSgdV3EhrhPBBDCMuDw_BVhQagLCKAQrwrlF0Xjh5nSOuW4ENzDY52imdZZEsdL4vd9bQC0uTA"


def main():

    st.session_state['token'] = t

    st.write("Relatório de Lançamentos")
    # Carregar dados de hotéis
    hoteis = pd.read_csv("https://raw.githubusercontent.com/Geanderson-Ferreira/open-data-base/main/hoteis.csv")['idHoteis']

    # Inputs na sidebar
    filter_hotel = st.sidebar.selectbox("Hotel", hoteis)
    data_inicial = st.sidebar.date_input("Data Inicial", datetime.datetime.now() - datetime.timedelta(days=1))
    data_final = st.sidebar.date_input("Data Final", datetime.datetime.now() - datetime.timedelta(days=1))

    # CRIAR DF
    # dados = get_transactions(hotel, inicio, fim, st.session_state['token'], limit="3000")
    dados = get_transactions(filter_hotel, data_inicial, data_final, st.session_state['token'], limit="3000")
    if 'journalPostings' in dados and 'postings' in dados['journalPostings']:
        data = dados['journalPostings']['postings']
    df = pd.json_normalize(data)
    df = df.fillna('')


    #----------------- Criação de DFs para Joins
    #----------------- transactionName / cashierNames
    df_transaction_names = pd.DataFrame(get_transaction_names(filter_hotel, st.session_state['token']))
    if 'cashier_names' not in st.session_state:
        st.session_state['cashier_names'] = pd.DataFrame(get_user_names(st.session_state['token'], filter_hotel))

    

    #------------ Filtro de negativos
    filter_negativos = st.sidebar.checkbox("Filtrar por Negativos", value=False, key=None, help=None, on_change=None, disabled=False, label_visibility="visible")
    if filter_negativos:
        df = df[df['transactionAmount'] < 0]

    #------------- Filtro de Grupo de Receita
    if 'transaction_groups' not in st.session_state:
        st.session_state['transaction_groups'] = get_transaction_groups(filter_hotel, st.session_state['token']) 
    filter_revenue_group = st.sidebar.selectbox("Grupo de Receita", ["Todos"] + sorted(st.session_state['transaction_groups']))
    
    if filter_revenue_group != 'Todos':
        codes_to_filter = get_codes_by_group(filter_hotel, st.session_state['token'], st.session_state['transaction_groups'][filter_revenue_group])
        df = df[df['transactionCode'].isin(codes_to_filter)]
    
    #------------ JOINS
    df = df.set_index('transactionCode').join(df_transaction_names.set_index('codes'))
    df = df.set_index('cashierInfo.cashierId').join(st.session_state['cashier_names'].set_index('cahierId'))


    #------------ Filtro transaction Types
    transaction_type_filter = st.sidebar.selectbox("Tipo de Transação", ["Todos"] + sorted(df["transactionType"].unique()))
    if transaction_type_filter != "Todos":
        df = df[df['transactionType'] == transaction_type_filter]

    #------------- Filtro de Transaction code Name
    transaction_name_filter = st.sidebar.selectbox("Código de Transação", ["Todos"] + sorted(df["transactionCodeName"].unique()))


    #----------- Filtro de usuários
    cashier_name_filter = st.sidebar.selectbox("Usuário", ["Todos"] + sorted(df["cashierName"].unique()))
    if cashier_name_filter != 'Todos':
        df = df[df['cashierName'] == cashier_name_filter]

    st.dataframe(df, hide_index=True)


if __name__ == "__main__":
    main()