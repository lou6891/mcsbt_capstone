import streamlit as st
import requests
import extra_streamlit_components as stx
import os
from dotenv import load_dotenv
import pandas as pd
from utils.verify_api_token import verify_api_token
import altair as alt

load_dotenv()
df = None
cookie_manager = stx.CookieManager(key="Customers_page")
st.title("Customers Dashboard")


@st.cache_data(show_spinner=False)
def api_call_customers(token):
    url = os.getenv("BASE_API_URL") + "api/v1/customers"
    res = requests.get(url, headers={"Authorization": "Bearer " + str(token)})
    return res


# API Call, first verify that the token is valid, if not get a new one, if not re login
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
        st.write("errror token validity")

if df is not None:
    #####################################################################
    # ############# FILTER FILTER FILTER FILTER FILTER ################ #
    #####################################################################
    st.sidebar.write("FILTERS")

    # Select specific customer id
    customer_id_lst = df["customer_id"]
    customer_id_filter = st.sidebar.text_input('Search a single customer id')
    st.sidebar.write('The current customer id selected is: ', customer_id_filter)

    # Sales channels filter
    gender_lst = df["gender"].unique()

    gender_filtered_lst = st.sidebar.multiselect(
        label="Gender Filter",
        options=gender_lst,
        default=gender_lst,
        key="multiselect_genders"
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

    mask = filtered_df['gender'].isin(gender_filtered_lst)
    filtered_df = filtered_df[mask]

    mask = (filtered_df['age'] > age_filtered_lst[0]) & (filtered_df['age'] < age_filtered_lst[1])
    filtered_df = filtered_df[mask]

    if len(customer_id_filter) > 0:
        filtered_df2 = filtered_df.loc[filtered_df["customer_id"] == customer_id_filter]
    else:
        filtered_df2 = filtered_df

    filtered_df2 = filtered_df2.reset_index(drop=True)
    st.dataframe(filtered_df2, use_container_width=True)

    #####################################################################
    # ###############  KPIS  KPIS  KPIS  KPIS  KPIS  ################## #
    #####################################################################

    kpi1, kpi2, kpi3 = st.columns(3)

    kp1_value = filtered_df2[filtered_df2["gender"] == "male"]
    kpi1.metric(
        label="Number of males customers",
        value=len(kp1_value),
        delta=len(kp1_value),
    )

    kp2_value = filtered_df2[filtered_df2["gender"] == "female"]
    kpi2.metric(
        label="Number of female customers",
        value=len(kp2_value),
        delta=len(kp2_value),
    )

    kp3_value = filtered_df2["age"].mean()
    kpi3.metric(
        label="Average age",
        value=round(kp3_value, 2),
        delta=-10 + kp3_value,
    )

    # Group the data by age and gender and count the number of occurrences
    grouped = filtered_df2.groupby(['age', 'gender']).size().reset_index(name='count')

    # Create the bar chart with Altair
    chart = alt.Chart(grouped).mark_bar().encode(
        x='age:O',
        y='count:Q',
        color='gender:N'
    ).properties(
        width=600,
        height=400
    )

    # Display the chart in Streamlit
    st.write("Number of customer id for each age, by gender")
    st.altair_chart(chart, use_container_width=True)
