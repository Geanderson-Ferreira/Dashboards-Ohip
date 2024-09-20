import streamlit as st
import pandas as pd

def checkin_panel():

    # Função para ser chamada ao clicar no ícone de edição
    def getResv(ResvId):
        st.write(f"Função getResv chamada com ResvId: {ResvId}")
        st.error("teste")
        return

    # Dados de exemplo
    data = {
        'ResvId': [1, 2, 3, 4],
        'Name': ['John Doe', 'Jane Doe', 'Alice', 'Bob'],
        'Room': ['101', '102', '103', '104']
    }

    df = pd.DataFrame(data)

    # Exibir a tabela com botões de edição
    st.write("Tabela de Reservas")
    for index, row in df.iterrows():
        cols = st.columns([1, 1, 1, 1, 1])
        if cols[0].button('Editar', key=row['ResvId']):
            getResv(row['ResvId'])
        cols[1].write(row['ResvId'])
        cols[2].write(row['Name'])
        cols[3].write(row['Room'])
        



# import streamlit as st
# from src.reservations.get_reservations import get_reservations
# import pandas as pd
# from flatten_json import flatten

# def checkin_panel():

#     st.title("Checkin")
#     hoteis = pd.read_csv("https://raw.githubusercontent.com/Geanderson-Ferreira/open-data-base/main/hoteis.csv")['idHoteis']
#     filter_hotel = st.sidebar.selectbox("Hotel", hoteis)

#     dados = get_reservations(filter_hotel, st.session_state['token'], {'expectedArrivals':'true'})
#     df = pd.DataFrame((flatten(x) for x in dados['reservations']['reservationInfo']))

#     st.dataframe(df)
#     st.write(dados)
    