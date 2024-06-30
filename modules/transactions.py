import streamlit as st
from src.transactions.get_transactions import get_transactions
from src.transactions.get_transaction_codes import get_transaction_names
from src.transactions.get_cashier_names import get_user_names
from src.transactions.get_transaction_groups import get_transaction_groups
from src.transactions.get_transaction_codes_by_group import get_codes_by_group
from src.utils import to_money
import pandas as pd
import datetime
import plotly.express as px


def transactions_dash():

    limit_allowed_return_transactions = "50000"
    limit_of_interval_of_dates_inputs = 15

    st.title("Revenue Viewer")
    st.sidebar.title("Obter Dados")
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

    st.sidebar.divider()
    st.sidebar.title("Partições")

    if 'data_final' in st.session_state:
        if filter_hotel != st.session_state['filter_hotel'] or data_inicial != st.session_state['data_inicial'] or data_final != st.session_state['data_final']:
            dados = get_transactions(filter_hotel, data_inicial, data_final, st.session_state['token'], limit=limit_allowed_return_transactions)
            st.session_state['dados'] = dados
            print("Segunda vez.")
            st.session_state['data_final'] = data_final
            st.session_state['data_inicial'] = data_inicial
            st.session_state['filter_hotel'] = filter_hotel
    else:
        st.session_state['data_final'] = data_final
        st.session_state['data_inicial'] = data_inicial
        st.session_state['filter_hotel'] = filter_hotel
        dados = get_transactions(filter_hotel, data_inicial, data_final, st.session_state['token'], limit=limit_allowed_return_transactions)
        print("Primeira vez")
        st.session_state['dados'] = dados

    dados = st.session_state['dados']
    # CRIA DF
    # dados = get_transactions(filter_hotel, data_inicial, data_final, st.session_state['token'], limit=limit_allowed_return_transactions)

    #------------- Validação do total de resultados (Só mostra se obter tudo)
    if dados['totalResults'] > int(limit_allowed_return_transactions):
        st.error(f"Consulta retornou mais que {int(limit_allowed_return_transactions)} registros, reduza seu filtro.")
        return

    if dados['totalResults'] == 0:
        st.info(f"Sua consulta não retornou nenhum dado.")
        return

    else:

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
        filter_negativos = st.sidebar.checkbox("Filtrar por Estornos", value=False, key=None, help=None, on_change=None, disabled=False, label_visibility="visible")
        if filter_negativos:
            # df= df[((df['transactionAmount'] < 0) & (df['transactionType'] == 'Revenue')) | ((df['transactionAmount'] > 0) & (df['transactionType'] == 'Payment'))]
            df = df[df['transactionAmount'] < 0]

        #------------- Filtro de Grupo de Receita
        if 'transaction_groups' not in st.session_state:
            st.session_state['transaction_groups'] = get_transaction_groups(filter_hotel, st.session_state['token']) 
        filter_revenue_group = st.sidebar.selectbox("Grupo de Receita", ["Todos"] + sorted(st.session_state['transaction_groups']))

        if filter_revenue_group != 'Todos':
            codes_to_filter = get_codes_by_group(filter_hotel, st.session_state['token'], st.session_state['transaction_groups'][filter_revenue_group])
            df = df[df['transactionCode'].isin(codes_to_filter)]
        
        #------------ JOINS
        # df.join(df_transaction_names.set_index('codes'), on='transactionCode')

        df = df.set_index('transactionCode').join(df_transaction_names.set_index('codes'))
        df = df.set_index('cashierInfo.cashierId').join(st.session_state['cashier_names'].set_index('cahierId'))

        #------------ Filtro transaction Types
        transaction_type_filter = st.sidebar.selectbox("Tipo de Transação", ["Todos"] + sorted(df["transactionType"].unique()))
        if transaction_type_filter != "Todos":
            df = df[df['transactionType'] == transaction_type_filter]

        #------------- Filtro de Transaction code Name
        transaction_name_filter = st.sidebar.selectbox("Código de Transação", ["Todos"] + sorted(df["transactionCodeName"].unique()))
        if transaction_name_filter != "Todos":
            df = df[df['transactionCodeName'] == transaction_name_filter]

        #----------- Filtro de usuários
        cashier_name_filter = st.sidebar.selectbox("Usuário", ["Todos"] + sorted(df["cashierName"].unique()))
        if cashier_name_filter != 'Todos':
            df = df[df['cashierName'] == cashier_name_filter]

        # --------------- Valores agrupados por código de lançamento

        title_1 = f"Receita de {filter_revenue_group} - {data_inicial} a {data_final}"
        df_grouped_by_code = df.groupby(['postingDate', "transactionCodeName"])["transactionAmount"].sum().reset_index()
        fig_prod = px.bar(df_grouped_by_code, 
                        x='transactionCodeName', 
                        y="transactionAmount", 
                        color="transactionCodeName",
                        title=title_1,
                        orientation="v")
        st.plotly_chart(fig_prod, use_container_width=False)

        st.sidebar.write("Nº Resultados:", dados['totalResults'])


        # --------------- Valores agrupados por dia da semana
        sorter_day_of_week = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        df["dayOfWeek"] = pd.Categorical(df["dayOfWeek"], categories=sorter_day_of_week, ordered=True)

        df_grouped_by_day_of_week = df.groupby(["dayOfWeek", "transactionCodeName"])["transactionAmount"].sum().reset_index()
        fig_prod_2 = px.bar(df_grouped_by_day_of_week.sort_values("dayOfWeek"), 
                        x="dayOfWeek", 
                        y="transactionAmount", 
                        color="transactionCodeName",
                        title="Detalhamento por dia da semana",
                        orientation="v")

        st.plotly_chart(fig_prod_2, use_container_width=True)


        df['transactionDate'] = pd.to_datetime(df['transactionDate']).dt.strftime("%d/%m/%Y")
        df['postingDate'] = pd.to_datetime(df['postingDate']).dt.strftime("%d/%m/%Y")
        df['revenueDate'] = pd.to_datetime(df['revenueDate']).dt.strftime("%d/%m/%Y")
        df['transactionNo'] = df['transactionNo'].astype(str)
        df['transactionAmount'] = df['transactionAmount'].apply(to_money)

        #---------------- Show dataframe
        cols_to_show = ["transactionDate", "transactionCodeName", "transactionAmount", "reference", "remark", "guestInfo.guestName", "guestInfo.roomId", "guestInfo.confirmationNo"]

        st.write("Relatório de Lancamentos")
        st.dataframe(df[cols_to_show], hide_index=True, use_container_width=True)
