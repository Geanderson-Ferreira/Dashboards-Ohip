import streamlit as st
from src.get_transactions import get_transactions
from src.auth import authenticate_this
from src.get_transaction_codes import get_transaction_names
from src.get_cashier_names import get_user_names
from src.get_transaction_groups import get_transaction_groups
from src.get_transaction_codes_by_group import get_codes_by_group
import pandas as pd
import datetime

st.set_page_config(layout="wide")

def main():

    limit_allowed_return_transactions = "50000"
    limit_of_interval_of_dates_inputs = 15

    st.write("Relatório de Lançamentos")
    # Carregar dados de hotéis
    hoteis = pd.read_csv("https://raw.githubusercontent.com/Geanderson-Ferreira/open-data-base/main/hoteis.csv")['idHoteis']

    # Inputs na sidebar
    filter_hotel = st.sidebar.selectbox("Hotel", hoteis)
    data_inicial = st.sidebar.date_input("Data Inicial", datetime.datetime.now() - datetime.timedelta(days=1))
    data_final = st.sidebar.date_input("Data Final", datetime.datetime.now() - datetime.timedelta(days=1))

    #-------------------- Validações de Data
    if data_final < data_inicial:
        st.error("Data inicial não pode ser maior do que data final.")
        return
    if data_inicial > datetime.datetime.now().date() or data_final > datetime.datetime.now().date():
        st.error("Não há lançamentos no futuro. Não viajamos no tempo.")
        return
    if (data_final - data_inicial).days > limit_of_interval_of_dates_inputs:
        st.error(f"Período máximo permitido {limit_of_interval_of_dates_inputs} dias.")
        return

    # CRIA DF
    dados = get_transactions(filter_hotel, data_inicial, data_final, st.session_state['token'], limit=limit_allowed_return_transactions)

    #------------- Validação do total de resultados (Só mostra se obter tudo)
    if dados['totalResults'] > int(limit_allowed_return_transactions):
        st.error(f"Consulta retornou mais que {int(limit_allowed_return_transactions)} registros, reduza seu filtro.")
        return

    if dados['totalResults'] == 0:
        st.info(f"Sua consulta não retornou nenhum dado.")
        return

    else:
        st.write(dados['totalResults'])

        if 'journalPostings' in dados and 'postings' in dados['journalPostings']:
            data = dados['journalPostings']['postings']
        df = pd.json_normalize(data)
        df = df.fillna('')

        df['transactionDate'] = pd.to_datetime(df['transactionDate'])
        df['postingDate'] = pd.to_datetime(df['postingDate'])
        df['revenueDate'] = pd.to_datetime(df['revenueDate'])

        df['dayOfWeek'] = df['postingDate'].dt.day_name()

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
    authenticate_this(main)