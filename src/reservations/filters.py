import streamlit as st
from src.reservations.search_types import search_types
import pandas as pd

def show_filters():
    hoteis = pd.read_csv("https://raw.githubusercontent.com/Geanderson-Ferreira/open-data-base/main/hoteis.csv")['idHoteis']
    
    filter_hotel = st.sidebar.selectbox("Hotel", hoteis)
    arrival_from = st.sidebar.date_input("Arrival From", value=None)
    arrival_to = st.sidebar.date_input("Arrival To", value=None)
    departure_from = st.sidebar.date_input("Departure From", value=None)
    departure_to = st.sidebar.date_input("Departure to", value=None)
    created_on = st.sidebar.date_input("Created On", value=None)
    confirmation_number_list = st.sidebar.text_input("Confirmation Number List")
    external_reference_ids = st.sidebar.text_input("External Reference List")

    st.sidebar.write("Types")
    for search_type in search_types:
        globals()[search_types[search_type]] = st.sidebar.checkbox(search_type)

    todays_cancellation = st.sidebar.checkbox("Cancelled today")
    early_departures = st.sidebar.checkbox("Early Departures")
    expected_arrivals = st.sidebar.checkbox("Arrivals Expected")
    expected_departures = st.sidebar.checkbox("Departures Expected")
    extended_stays = st.sidebar.checkbox("Extended Stays")

    data_to_search = {
        "hotelId": filter_hotel,
        "arrivalStartDate": arrival_from, "arrivalEndDate": arrival_to,
        "departureStartDate": departure_from, "departureEndDate": departure_to,
        "createdOn": created_on, "confirmationNumberList": confirmation_number_list.split(","),
        "externalReferenceIds": external_reference_ids.split(","),
        "dayOfArrivalCancels": todays_cancellation,
        "earlyDepartures": early_departures, "expectedArrivals": expected_arrivals,
        "expectedDepartures": expected_departures, "extendedStays": extended_stays
    }
    data_to_search['searchType'] = list()
    for key, val in search_types.items():

        if globals()[search_types[key]]:
            data_to_search['searchType'].append(search_types[key])
    
    return data_to_search