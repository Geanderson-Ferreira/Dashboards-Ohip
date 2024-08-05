import streamlit as st
from src.tcpos.tcpos import get_df_pandas_tcpos_transactions

def show_tcpos_data(data_inicial, data_final, filter_hotel):
    st.sidebar.divider()
    st.sidebar.title("Filtros TCPOS")
    st.title("Relatório de Lancamentos (TCPOS)")
    df_tcpos = get_df_pandas_tcpos_transactions(data_inicial, data_final, filter_hotel)

    st.dataframe(df_tcpos, hide_index=True)