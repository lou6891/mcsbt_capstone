import streamlit as st
import requests
import extra_streamlit_components as stx
import os
from dotenv import load_dotenv
import pandas as pd
from utils.verify_api_token import verify_api_token
import altair as alt
from streamlit_extras.app_logo import add_logo

load_dotenv()
df = None

try:
    # Config page title and icon
    st.set_page_config(page_title="H&M Analytics", page_icon=":bar_chart:")
except Exception as error:
    pass;

# set logo
add_logo("./img/logo_small.png", height=200)

cookie_manager = stx.CookieManager(key="Customers_page")

st.title("Customers Dashboard")


@st.cache_data(show_spinner=False)
def api_call_customers(token):
    url = os.getenv("BASE_API_URL") + "api/v1/customers"
    res = requests.get(url, headers={"Authorization": "Bearer " + str(token)})
    return res


# API Call, first verify that the token is valid, if not get a new one, if not re login
# Not created a universal function cause I want to cache the data of each page

with st.spinner('Verifying token ...'):
    token = verify_api_token()
    if token:
        with st.spinner('Wait for data...'):
            response = api_call_customers(token)

        if response.ok:
            df = pd.DataFrame(response.json()["result"])
        else:
            st.write(response)
    else:
        st.write("Refreshing Token")

if df is not None:

    #####################################################################
    # ############# FILTER FILTER FILTER FILTER FILTER ################ #
    #####################################################################
    st.sidebar.write("FILTERS")

    # Select specific customer id
    customer_id_lst = df["customer_id"]
    customer_id_filter = st.sidebar.text_input('Search a single customer id')
    st.sidebar.write('The current customer id selected is: ', customer_id_filter)

    # Select specific customer id
    postal_code_lst = df["postal_code"]
    postal_code_filter = st.sidebar.text_input('Search a postal code')
    st.sidebar.write('The current customer id selected is: ', postal_code_filter)

    club_member_status_lst = df["club_member_status"].unique()

    club_member_status_filtered_lst = st.sidebar.multiselect(
        label="Club Member Status Filter",
        options=club_member_status_lst,
        default=club_member_status_lst,
        key="multiselect_club_member_status"
    )

    # price range filter
    age_lst = df["age"]

    min_age = int(age_lst.min())
    max_age = int(age_lst.max())

    age_filtered_lst = st.sidebar.slider(
        'Select age range',
        min_age, max_age, (min_age, max_age))

    st.sidebar.write('Age range selected:\n', age_filtered_lst)

    # Modify the df
    filtered_df = df.copy()

    mask = filtered_df['club_member_status'].isin(club_member_status_filtered_lst)
    filtered_df = filtered_df[mask]

    mask = (filtered_df['age'] >= age_filtered_lst[0]) & (filtered_df['age'] <= age_filtered_lst[1])

    filtered_df = filtered_df[mask]

    if len(customer_id_filter) > 0:
        filtered_df2 = filtered_df.loc[filtered_df["customer_id"] == customer_id_filter]
    else:
        filtered_df2 = filtered_df

    if len(postal_code_filter) > 0:
        filtered_df3 = filtered_df2.loc[filtered_df["postal_code"] == postal_code_filter]
    else:
        filtered_df3 = filtered_df2

    filtered_df3 = filtered_df3.reset_index(drop=True)
    st.dataframe(filtered_df3, use_container_width=True)

    #####################################################################
    # ###############  KPIS  KPIS  KPIS  KPIS  KPIS  ################## #
    #####################################################################

    kpi1, kpi2, kpi3 = st.columns(3)

    kp1_value = filtered_df3["customer_id"].unique()
    delta_kp1 = len(kp1_value) - len(df["customer_id"].unique())
    kpi1.metric(
        label="Number of unique customer IDs",
        value=len(kp1_value),
        delta=delta_kp1,
    )

    kp2_value = filtered_df3["postal_code"].unique()
    delta_kp2 = len(kp2_value) - len(df["postal_code"].unique())
    kpi2.metric(
        label="Number of unique postal codes",
        value=len(kp2_value),
        delta=delta_kp2,
    )

    kp3_value = filtered_df3["age"].mean()
    delta_kp3 = round(kp3_value, 2) - round(df["age"].mean(), 2)
    kpi3.metric(
        label="Average age",
        value=round(kp3_value, 2),
        delta=delta_kp3,
    )

    # Group the data by club member status and count the number of unique customer IDs
    grouped = filtered_df3.groupby('club_member_status')['customer_id'].nunique()
    # Get unique club_member_status values
    domain_values = filtered_df3["club_member_status"].unique()
    # Create a bar chart using Altair
    chart = alt.Chart(grouped.reset_index()).mark_bar().encode(
        x='club_member_status',
        y='customer_id',
        color=alt.Color('club_member_status', scale=alt.Scale(domain=domain_values, range=['red', 'lightsalmon']))
    )

    # Display the chart in Streamlit
    st.altair_chart(chart, use_container_width=True)
