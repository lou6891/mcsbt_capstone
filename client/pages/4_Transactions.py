import streamlit as st
import requests
import extra_streamlit_components as stx
import os
from dotenv import load_dotenv
import pandas as pd
from utils.verify_api_token import verify_api_token
import altair as alt
from utils.add_logo import add_logo


load_dotenv()
df = None
try:
    # Config page title and icon
    st.set_page_config(page_title="H&M Analytics", page_icon=":bar_chart:")
except Exception as error:
    pass;

# set logo
add_logo(300, 170)

cookie_manager = stx.CookieManager(key="Transactions_page")

st.title("Transactions Dashboard")


@st.cache_data(show_spinner=False)
def api_call_transactions(token):
    url = os.getenv("BASE_API_URL") + "api/v1/transactions"
    res = requests.get(url, headers={"Authorization": "Bearer " + str(token)})
    return res


# API Call, first verify that the token is valid, if not get a new one, if not re login
# Not created a universal function cause I want to cache the data of each page

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
        st.write("Refreshing Token")

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
        'Select a price range',
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
    delta_kp1 = len(kp1_value) - len(df["customer_id"].unique())
    kpi1.metric(
        label="Number of different customers",
        value=len(kp1_value),
        delta=delta_kp1,
    )

    kp2_value = filtered_df2["sales_channel_id"].unique()
    delta_kp2 = len(kp2_value) - len(df["sales_channel_id"].unique())
    kpi2.metric(
        label="Number of different sales channels",
        value=len(kp2_value),
        delta=delta_kp2,
    )

    kp3_value = filtered_df2["price"].mean()
    delta_kp3 = round(kp3_value, 2) - round(df["price"].mean(), 2)
    kpi3.metric(
        label="Average price",
        value=round(kp3_value, 2),
        delta=round(delta_kp3, 2),
    )

    kpi4, kpi5 = st.columns(2)

    if len(filtered_df2["t_dat"]) > 0:
        kp4_value = (max(filtered_df2["t_dat"]) - min(filtered_df2["t_dat"])).days
        old_value = (max(df["t_dat"]) - min(df["t_dat"])).days
    else:
        kp4_value = 0
        old_value = 0
    delta_kp4 = old_value - kp4_value
    kpi4.metric(
        label="Number of days for the date range selected",
        value=kp4_value,
        delta=delta_kp4,
    )

    if filtered_df2['customer_id'].notnull().any():
        kp5_value = int(filtered_df2['customer_id'].value_counts().max())
    else:
        kp5_value = 0
    old_value = int(df['customer_id'].value_counts().max())
    delta_kp5 = kp5_value - old_value
    kpi5.metric(
        label="Highest number of transactions by a unique client",
        value=kp5_value,
        delta=delta_kp5,
    )

    # calculate count of unique transaction IDs and get top 10
    histdf = pd.DataFrame(pd.Series(df['customer_id'].value_counts()).nlargest(25))

    # Create a new column with index values
    # Reset the index and rename the columns
    histdf.reset_index(inplace=True)
    histdf.columns = ['customer_id', 'count']

    # Create a new column 'row_number' containing the row numbers
    histdf['row_number'] = range(len(histdf))

    # Create a new column 'color' with alternating values of 'red' and 'lightsalmon'
    histdf['color'] = histdf['row_number'].apply(lambda x: 'red' if x % 2 == 0 else 'lightsalmon')

    # create an Altair chart
    chart = alt.Chart(histdf).mark_bar(size=15).encode(
        x='count:Q',
        y=alt.Y('customer_id:N', sort='-x'),
        color=alt.Color('color:N', scale=None, legend=None)
    )

    # display the chart in Streamlit
    st.write("Customers with highest transaction count")
    st.altair_chart(chart, use_container_width=True)
