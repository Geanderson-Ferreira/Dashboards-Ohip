import streamlit as st
from src.tcpos.tcpos import get_df_pandas_tcpos_transactions
import pandas as pd
import plotly.express as px

def show_tcpos_data(data_inicial, data_final, filter_hotel):
    st.sidebar.divider()
    st.sidebar.title("Filtros TCPOS")
    st.title("Relatório de Lancamentos (TCPOS)")
    df = get_df_pandas_tcpos_transactions(data_inicial, data_final, filter_hotel)

    df['transDate'] = pd.to_datetime(df['transDate'])
    df['Date'] = df['transDate'].dt.date
    df['Time'] = df['transDate'].dt.time
    df['dayOfWeek'] = df['transDate'].dt.day_name()

    st.dataframe(df, hide_index=True)


    #------------------ Relatório TCPOS dias da semana segmentado por itens lançados
    sorter_day_of_week = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    df["dayOfWeek"] = pd.Categorical(df["dayOfWeek"], categories=sorter_day_of_week, ordered=True)

    df_grouped_by_day_of_week = df.groupby(["dayOfWeek", "articleDescription"])["amountGross"].sum().reset_index()
    fig_prod_2 = px.bar(df_grouped_by_day_of_week.sort_values("dayOfWeek"), 
                    x="dayOfWeek", 
                    y="amountGross", 
                    color="articleDescription",
                    title="Receita TCPOS por dia da semana",
                    orientation="v")

    st.plotly_chart(fig_prod_2, use_container_width=True)



    title_1 = f"Titulo"
    df_grouped_by_code = df.groupby(["articleDescription"])["quantity"].sum().reset_index()

    fig_prod = px.bar(df_grouped_by_code.sort_values("quantity").tail(30), 
                    x='articleDescription', 
                    y="quantity", 
                    color="articleDescription",
                    title=title_1,
                    orientation="v")
    st.plotly_chart(fig_prod, use_container_width=False)


    st.write(df.dtypes)