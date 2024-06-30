import streamlit as st
from src.reservations.get_reservations import get_reservations
from src.reservations.filters import show_filters
from src.profiles.get_profiles_by_ids import get_profiles_by_ids
import pandas as pd
from flatten_json import flatten


def reservations_dash():
    st.session_state['token'] = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsIng1dCI6IjFCZUYycEpFQWQtY3g2d3BnU3IyTkFZbkVtdyIsImtpZCI6Im1zLW9hdXRoa2V5In0.eyJzdWIiOiJpbnRlZ3JhY2FvX2dlYW5kZXJzb24iLCJpc3MiOiJ3d3cub3JhY2xlLmNvbSIsIm9yYWNsZS5vYXV0aC5zdmNfcF9uIjoiT0F1dGhTZXJ2aWNlUHJvZmlsZSIsImlhdCI6MTcxOTc2MTE2OCwib3JhY2xlLm9hdXRoLnBybi5pZF90eXBlIjoiTERBUF9VSUQiLCJleHAiOjE3MTk3NjQ3NjgsIm9yYWNsZS5vYXV0aC50a19jb250ZXh0IjoidXNlcl9hc3NlcnRpb24iLCJhdWQiOlsiaHR0cHM6Ly8qb3JhY2xlKi5jb20iLCJodHRwczovLyouaW50ICIsImh0dHBzOi8vKm9jcy5vYy10ZXN0LmNvbS8iXSwicHJuIjoiaW50ZWdyYWNhb19nZWFuZGVyc29uIiwianRpIjoiZDBkYTU3ODAtMzYxOS00NmE5LWFhZDktOWU5NjY3NGMxNTFhIiwib3JhY2xlLm9hdXRoLmNsaWVudF9vcmlnaW5faWQiOiJBQ0NPUkFUX0NsaWVudCIsInVzZXIudGVuYW50Lm5hbWUiOiJEZWZhdWx0RG9tYWluIiwib3JhY2xlLm9hdXRoLmlkX2RfaWQiOiIxMjM0NTY3OC0xMjM0LTEyMzQtMTIzNC0xMjM0NTY3ODkwMTIifQ.Kr_f0K8mSpAmrroKHEXpyJPQKlD5EN74KRNRTECdH-cSx7IdJm_EQd1qIUAVFrJPebI5AqNHYrbGi31OCGIkOlg8TPBuD3VUUEOLU80Ge6Lii-rRm9lpSZt9mmA6vvvQSE0uZTWjG_3pY-RR10Gl3XhAMyuCPBxH9O0YHY87SfFfg7Avkop4Y8fWtAn2vbs2GLmKPG_9nk4wH0iPMKLoQCLKiVXcjkNkAhvHSUp5vNNnxRdv6SiRNBcD38Czhex3V7FwB2OjGmeqDl-3_YKmsIe4NCDgieTLKzc8mvLHWx7cguoWwCWDbzpCcJhyWVRYJ_vJVnncWxNn0DBXaJNkEw"

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
