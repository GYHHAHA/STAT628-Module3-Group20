import folium
from streamlit_folium import st_folium
import streamlit as st
import pandas as pd
import numpy as np


if __name__ == "__main__":

    shop = pd.read_pickle("../data/raw_business.pkl")
    shop = shop.drop_duplicates(
        ["state", "city", "name", "address"], keep="first",
    ).reset_index(drop=True)
    review = pd.read_pickle("../data/raw_review.pkl")

    data = {
        state: {
            city: {
                name: {
                    address
                    for address in shop[
                        (shop.state==state)
                        & (shop.city==city)
                        & (shop.name==name)
                    ].address.unique()
                }
                for name in shop[
                    (shop.state==state)
                    & (shop.city==city)
                ].name.unique()
            }
            for city in shop[shop.state==state].city.unique()
        }
        for state in shop.state.unique()
    }

    st.markdown(
        """
        <style>
        .sidebar .sidebar-content {
            background-color: #011839;
            background-image: none;
            color: #ffffff
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.title("Suggestions for Taco Restaurants")
    st.sidebar.image("taco.jpg", width=200)
    st.sidebar.write(
        """
        This app is maintained by Group-20 
        (YUANHAO GENG, ???, ??? and ???).
        If you have any question about this app, 
         please contact us through geng29@wisc.edu.
        """
    )

    # Using object notation
    state = st.sidebar.selectbox(
        "Please Select the State:",
        data.keys(),
    )
    city = st.sidebar.selectbox(
        "Please Select the City:",
        data[state].keys(),
    )
    name = st.sidebar.selectbox(
        "Please Select the Restaurants Name:",
        data[state][city].keys(),
    )
    address = st.sidebar.selectbox(
        "Please Select the Address:",
        data[state][city][name],
    )

    hide_table_row_index = """
        <style>
        thead tr th:first-child {display:none}
        tbody th {display:none}
        </style>
        """
    st.markdown(hide_table_row_index, unsafe_allow_html=True)

    pros, cons = ["adsf", "waef", "ewfae"], ["adsf", "waef", "ewfae"]
    st.title("Suggestion")
    st.write("**Name**: " + name)
    st.write("**Address**: " + address)
    st.write("**Pros**:")
    for i in pros:
        st.markdown(f"- {i}")
    st.write("**Cons**:")
    st.markdown("".join([f"- {i} " for i in cons]))

    st.markdown('''
    <style>
    [data-testid="stMarkdownContainer"] ul{
        padding-left:40px;
    }
    </style>
    ''', unsafe_allow_html=True)

    st.title("Location")

    rec = shop[
        (shop.state==state)
        & (shop.city==city)
        & (shop.name==name)
        & (shop.address==address)
    ].iloc[0]
    loc = [rec["latitude"], rec["longitude"]]
    m = folium.Map(location=loc, zoom_start=16)
    folium.Marker(loc, popup=name, tooltip=name).add_to(m)
    st_data = st_folium(m, width=500, height=500)

    st.title("Ratings")
    business_id = "4IcB3QyMEA85UTWFKh9O9A"
    stars = review.query(f"business_id == '{business_id}'").stars
    stars = stars.value_counts().reindex(range(1, 6)).fillna(0)
    stars.name = "number of reviews"
    st.bar_chart(stars, height=300)
