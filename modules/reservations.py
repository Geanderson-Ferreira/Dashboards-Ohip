import streamlit as st
from src.reservations.get_reservations import get_reservations
from src.reservations.filters import show_filters
from src.profiles.get_profiles_by_ids import get_profiles_by_ids
import pandas as pd
from flatten_json import flatten

def reservations_dash():

    st.title("Reservations Exporter")

    #Apresentação dos filtros
    data_to_search = show_filters()

    #Gatilho da busca
    search = st.sidebar.button("Buscar")

    if search:

        #Constrói o dataFrame de reservas
        reservations = get_reservations(data_to_search['hotelId'], st.session_state['token'], data_to_search)
        if not reservations:
            return
        df_reservations = pd.DataFrame((flatten(d) for d in reservations['reservations']['reservationInfo']))

        #Constrói o dataframe de Profiles
        profile_ids = df_reservations['reservationGuest_id'].unique()
        profiles = get_profiles_by_ids(data_to_search['hotelId'], st.session_state['token'], profile_ids)
        if not profiles:
            return
        df_profiles = pd.json_normalize((flatten(d) for d in profiles['profiles']['profileInfo']))
        
        #Mostra o DataFrame de reservas
        st.subheader("Reservations")
        st.dataframe(df_reservations)

        st.subheader("Profiles")
        #Mostra o DataFrame de profiles
        st.dataframe(df_profiles)

        #Mostra os filtros aplicados
        st.write("Filtros aplicados")
        st.write({"filters": data_to_search})