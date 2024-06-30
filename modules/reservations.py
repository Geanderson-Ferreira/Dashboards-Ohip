import streamlit as st
from src.reservations.get_reservations import get_reservations
from src.reservations.filters import show_filters
import pandas as pd
from flatten_json import flatten

st.session_state['token'] = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsIng1dCI6IjFCZUYycEpFQWQtY3g2d3BnU3IyTkFZbkVtdyIsImtpZCI6Im1zLW9hdXRoa2V5In0.eyJzdWIiOiJpbnRlZ3JhY2FvX2dlYW5kZXJzb24iLCJpc3MiOiJ3d3cub3JhY2xlLmNvbSIsIm9yYWNsZS5vYXV0aC5zdmNfcF9uIjoiT0F1dGhTZXJ2aWNlUHJvZmlsZSIsImlhdCI6MTcxOTY5OTE1Mywib3JhY2xlLm9hdXRoLnBybi5pZF90eXBlIjoiTERBUF9VSUQiLCJleHAiOjE3MTk3MDI3NTMsIm9yYWNsZS5vYXV0aC50a19jb250ZXh0IjoidXNlcl9hc3NlcnRpb24iLCJhdWQiOlsiaHR0cHM6Ly8qb3JhY2xlKi5jb20iLCJodHRwczovLyouaW50ICIsImh0dHBzOi8vKm9jcy5vYy10ZXN0LmNvbS8iXSwicHJuIjoiaW50ZWdyYWNhb19nZWFuZGVyc29uIiwianRpIjoiMzQ2ODM2NGItMmI2Mi00YzdlLWI0Y2YtMzY0NDU5MjI4NzM5Iiwib3JhY2xlLm9hdXRoLmNsaWVudF9vcmlnaW5faWQiOiJBQ0NPUkFUX0NsaWVudCIsInVzZXIudGVuYW50Lm5hbWUiOiJEZWZhdWx0RG9tYWluIiwib3JhY2xlLm9hdXRoLmlkX2RfaWQiOiIxMjM0NTY3OC0xMjM0LTEyMzQtMTIzNC0xMjM0NTY3ODkwMTIifQ.HSJSGBmTKhS8S1jupmyVkp-hvN25HNRRfQpmUcQLJDnLSQ-4AsL50cBK-devbWA4fn85XFsqyLOQ2K3lXHDxfqaCzlGeL90LB5_cMM1zu7otbHSeWD4dJKvtIlQcq-u8GDdaFkvu-s5FqgsDztqQpetjwhjXKrLCeOsVRm3gV9JhCaP-5Z9mbS66FGckKsFx7XIIOx0OFdmrU4DoKxW3OJd0Kn12x1Hki0OsBvV5z_dCBvEusYer7NzOama7VC4pjxLfL-5nanUW_vmGeasCMomB5V1eqZEzbB2WP6QCx8aD4pene4TKhMUIC_ruT6YkwoyYiAMrOT-cU4R_TWBsTQ"

def reservations_dash():
    st.title("Reservations Exporter")

    #Apresentação dos filtros
    data_to_search = show_filters()

    #Gatilho da busca
    search = st.sidebar.button("Buscar")

    if search:
        #Consulta na API
        response = get_reservations(data_to_search['hotelId'], st.session_state['token'], data_to_search)
        dados = (flatten(d) for d in response['reservations']['reservationInfo'])
        
        #Constrói o dataFrame
        df = pd.DataFrame(dados)

        #Mostra o DataFrame

        st.dataframe(df)
        st.write("Filtros aplicados")
        st.write({"filters": data_to_search})
