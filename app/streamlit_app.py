import folium
from streamlit_folium import st_folium
from gsheetsdb import connect
import streamlit as st
import pandas as pd
import numpy as np


if __name__ == "__main__":

    @st.cache(
        hash_funcs={
            "_thread.RLock": lambda _: None,
            "builtins.weakref": lambda _: None,
        }
    )
    def load_data():
        def get_rows(name):
            conn = connect()
            def run_query(query):
                rows = conn.execute(query, headers=1)
                rows = rows.fetchall()
                return rows
            sheet_url = st.secrets[f"{name}_url"]
            return run_query(f'SELECT * FROM "{sheet_url}"')
        try:
            shop_rows = get_rows("shop")
            review_rows = get_rows("review")
            shop = pd.DataFrame(
                {
                    c: [r.__getattribute__(c) for r in shop_rows]
                    for c in [
                        'business_id', 'name', 'address', 'city',
                        'state', 'postal_code', 'latitude', 'longitude',
                        'stars', 'review_count', 'is_open', 'attributes',
                        'categories', 'hours'
                    ]
                }
            )
            review = pd.DataFrame(
                {
                    c: [r.__getattribute__(c) for r in review_rows]
                    for c in ['business_id', 'stars']
                }
            )
        except:
            shop = pd.read_pickle("../data/raw_business.pkl")
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
                        if address != ""
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
        return shop, review, data, [
            [[
                "Your service improves your ratings a lot!",
                "Your dish improves your ratings a lot!",
                "Your environment improves your ratings a lot!",
            ], [
                "Good to hear you have friendly waiters.",
                "Wow! Great to find that people like your shrimp dish!",
                "People are having great experience given your nice environment!",
            ]],
            [[
                "Too many complaints about waiting time!",
                "How about improving your service?",
                "You could make your dishes better!",
            ], [
                "Some guests are complaining that your beef is not good.",
                "Why don’t you try to make good environment?",
                "It will be better with improving your shrimp dish.",
            ]],
        ]

    shop, review, data, pc = load_data()
    shop = shop.drop_duplicates(
        ["state", "city", "name", "address"], keep="first",
    ).reset_index(drop=True)



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
    st.sidebar.image(st.secrets["taco_img"], width=200)
    st.sidebar.write(
        """
        This app is maintained by Group-20 
        (Yuanhao Geng, Xuelan Qian, Zhanpeng Xu and Xinyu Li).
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

    pros, cons = pc[0], pc[1]
    st.title("Suggestion")
    st.write("**Name**: " + name)
    st.write("**Address**: " + ("unknown" if address is None else address))
    np.random.seed(len(address) + len(name))
    a1, a2, a3, a4 = np.random.choice([0, 1, 2], 4)
    st.write("**Pros**:")
    st.markdown(f"- {pros[0][a1]}")
    st.markdown(f"- {pros[1][a2]}")
    st.write("**Cons**:")
    st.markdown(f"- {cons[0][a3]}")
    st.markdown(f"- {cons[1][a4]}")

    st.markdown('''
    <style>
    [data-testid="stMarkdownContainer"] ul{
        padding-left:40px;
    }
    </style>
    ''', unsafe_allow_html=True)

    st.title("Location")

    if (address == "None") or (address is None):
        address = ""
    rec = shop[
        (shop.state==state)
        & (shop.city==city)
        & (shop.name==name)
        & (shop.address.fillna("")==address)
    ].iloc[0]
    loc = [rec["latitude"], rec["longitude"]]
    m = folium.Map(location=loc, zoom_start=16)
    folium.Marker(loc, popup=name, tooltip=name).add_to(m)
    st_data = st_folium(m, width=500, height=500)

    st.title("Ratings")
    business_id = rec["business_id"]
    stars = review.query(f"business_id == '{business_id}'").stars
    stars = stars.value_counts().reindex(range(1, 6)).fillna(0)
    stars.name = "number of reviews"
    st.bar_chart(stars, height=300)
