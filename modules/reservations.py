import streamlit as st
from src.reservations.get_reservations import get_reservations
from src.reservations.filters import show_filters
from src.profiles.get_profiles_by_ids import get_profiles_by_ids
import pandas as pd
from flatten_json import flatten

def reservations_dash():
    st.session_state['token'] = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsIng1dCI6IjFCZUYycEpFQWQtY3g2d3BnU3IyTkFZbkVtdyIsImtpZCI6Im1zLW9hdXRoa2V5In0.eyJzdWIiOiJpbnRlZ3JhY2FvX2dlYW5kZXJzb24iLCJpc3MiOiJ3d3cub3JhY2xlLmNvbSIsIm9yYWNsZS5vYXV0aC5zdmNfcF9uIjoiT0F1dGhTZXJ2aWNlUHJvZmlsZSIsImlhdCI6MTcxOTc2NDg1MCwib3JhY2xlLm9hdXRoLnBybi5pZF90eXBlIjoiTERBUF9VSUQiLCJleHAiOjE3MTk3Njg0NTAsIm9yYWNsZS5vYXV0aC50a19jb250ZXh0IjoidXNlcl9hc3NlcnRpb24iLCJhdWQiOlsiaHR0cHM6Ly8qb3JhY2xlKi5jb20iLCJodHRwczovLyouaW50ICIsImh0dHBzOi8vKm9jcy5vYy10ZXN0LmNvbS8iXSwicHJuIjoiaW50ZWdyYWNhb19nZWFuZGVyc29uIiwianRpIjoiMjJiYjJhNjEtMDUzMS00YjE5LTg1ZTktNDI2ZmE1MWMzYTFmIiwib3JhY2xlLm9hdXRoLmNsaWVudF9vcmlnaW5faWQiOiJBQ0NPUkFUX0NsaWVudCIsInVzZXIudGVuYW50Lm5hbWUiOiJEZWZhdWx0RG9tYWluIiwib3JhY2xlLm9hdXRoLmlkX2RfaWQiOiIxMjM0NTY3OC0xMjM0LTEyMzQtMTIzNC0xMjM0NTY3ODkwMTIifQ.dHPe6MZQ9D2S24X_7ewzPoCiGyy1bxuZOduNZ2t-6gPGTw5SK2UkbL8RwtDyOvBDy3L5qtotWG_UDstoxYNoQ3-_RuBh0-qpFF5GcaghPNSM3sEhOMJDf_Hzcv-PyL2xtE1rs2a_hKffsc34EHyfrUi-4qs-bDHTlHV_Q2HXDcYo6CXgmPxPrsar9Jvq__WaMinOJ5TryXvkilKwK9LA4aU2viSPJ5GXXt2rRnxv1_O4Y6owRVlTbqvYI8UqKagApjc_r-e4YCnM8b_P7DbmbCj0dXtzpqWHdsDcLbh9Arw0yyw8eUt8UsBAsJNvVkcBybWAGGGINQCO6xfUGr7uYw"

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