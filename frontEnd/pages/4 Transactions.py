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
cookie_manager = stx.CookieManager(key="Transactions_page")
st.title("Transactions Dashboard")


@st.cache_data(show_spinner=False)
def api_call_transactions(token):
    url = os.getenv("BASE_API_URL") + "api/v1/transactions"
    res = requests.get(url, headers={"Authorization": "Bearer " + str(token)})
    return res


# API Call, first verify that the token is valid, if not get a new one, if not re login
with st.spinner('Verifying token ...'):
    token = verify_api_token()
    if token:
        with st.spinner('Wait for data...'):
            response = api_call_transactions(token)

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

    # Sales channels filter
    sales_channels_lst = df["sales_channel_id"].unique()

    sales_channels_filtered_lst = st.sidebar.multiselect(
        label="Sales Channels",
        options=sales_channels_lst,
        default=sales_channels_lst,
        key="multiselect_sales_channels"
    )

    # price range filter
    price_lst = df["price"]
    min_price = float(price_lst.min())
    max_price = float(price_lst.max())

    price_filtered_lst = st.sidebar.slider(
        'Select a range of ages',
        0.0, max_price, (min_price, max_price), format="%f", )

    st.sidebar.write('Price range selected:')
    st.sidebar.write(price_filtered_lst)


    # DATE range filter
    df["t_dat"] = pd.to_datetime(df['t_dat'])
    dates_list = df["t_dat"]
    min_date = min(dates_list)
    max_date = max(dates_list)

    start_date = st.sidebar.date_input('Select time range', (min_date, max_date), min_date, max_date)

    # Select specific customer id
    customer_id_lst = df["customer_id"]
    customer_id_filter = st.sidebar.text_input('Search a single customer id')
    st.sidebar.write('The current customer id selected is: ', customer_id_filter)

    # Modify the df
    filtered_df = df.copy()

    mask = filtered_df['sales_channel_id'].isin(sales_channels_filtered_lst)
    filtered_df = filtered_df[mask]

    mask = (filtered_df['price'] > price_filtered_lst[0]) & (filtered_df['price'] < price_filtered_lst[1])
    filtered_df = filtered_df[mask]

    mask = filtered_df['t_dat'].isin(dates_list)
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

    kp1_value = filtered_df2["customer_id"].unique()
    kpi1.metric(
        label="Number of different customers",
        value=len(kp1_value),
        delta=len(kp1_value),
    )

    kp2_value = filtered_df2["sales_channel_id"].unique()
    kpi2.metric(
        label="Number of different sales channels",
        value=len(kp2_value),
        delta=len(kp2_value),
    )

    kp3_value = filtered_df2["price"].mean()
    kpi3.metric(
        label="Average price",
        value=round(kp3_value, 2),
        delta=-10 + kp3_value,
    )

    kpi4, kpi5 = st.columns(2)
    date_lst = filtered_df2["t_dat"]
    dates_list = filtered_df2["t_dat"]
    kp4_value = (max(dates_list) - min(dates_list)).days
    kpi4.metric(
        label="Number of days for the date range selected",
        value=kp4_value,
        delta=kp4_value,
    )

    kp5_value = int(filtered_df2['customer_id'].value_counts().max())
    kpi5.metric(
        label="Highest number of transactions by a unique client",
        value=kp5_value,
        delta=kp5_value,
    )

    # calculate count of unique transaction IDs and get top 10
    histdf = pd.DataFrame(pd.Series(df['customer_id'].value_counts()).nlargest(25))
    # Create a new column with index values
    histdf['index'] = histdf.index

    # create an Altair chart
    chart = alt.Chart(histdf).mark_bar(size=15).encode(
        x='customer_id',
        y='index'
    )

    # display the chart in Streamlit
    st.write("Customers with highest transaction count")
    st.altair_chart(chart, use_container_width=True)
