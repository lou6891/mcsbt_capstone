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

cookie_manager = stx.CookieManager(key="Article_page")

st.title("Articles Dashboard")


def convert_object_to_string(df):
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].astype(str)

    return df


# API Call, first verify that the token is valid, if not get a new one, if not re login
# Not created a universal function cause I want to cache the data of each page
@st.cache_data(show_spinner=False)
def api_call_articles(token):
    url = os.getenv("BASE_API_URL") + "api/v1/articles"
    res = requests.get(url, headers={"Authorization": "Bearer " + str(token)})
    return res

with st.spinner('Verifying token ...'):
    token = verify_api_token()
    if token:
        with st.spinner('Wait for data...'):
            response = api_call_articles(token)

        if response.ok:
            df = pd.DataFrame(response.json()["result"])
            convert_object_to_string(df)
        else:
            st.write(response)
    else:
        st.write("Refreshing Token")


#####################################################################
# ############# FILTER FILTER FILTER FILTER FILTER ################ #
#####################################################################
if df is not None:

    st.sidebar.write("FILTERS")
    # print(df.dtypes)
    # for i in df.columns:
    #    print(i, len(df[i].unique()))

    # Select specific product code
    product_code_filter = st.sidebar.text_input('Search a single product code')
    st.sidebar.write('The current product code selected is: ', product_code_filter)

    # colour_group_name_lst filter
    garment_group_name_lst = df["garment_group_name"].unique()
    garment_group_name_filtered_lst = st.sidebar.multiselect(
        label="Select Garment Group",
        options=garment_group_name_lst,
        default=garment_group_name_lst,
        key="multiselect_garment_group_name",
    )

    # colour_group_name_lst filter
    product_group_name_lst = df["product_group_name"].unique()
    product_group_name_filtered_lst = st.sidebar.multiselect(
        label="Select Product Group",
        options=product_group_name_lst,
        default=product_group_name_lst,
        key="multiselect_product_group_name",
    )

    # colour_group_name_lst filter
    index_name_lst = df["index_name"].unique()

    index_name_lst_filtered_lst = st.sidebar.multiselect(
        label="Select Index Name",
        options=index_name_lst,
        default=index_name_lst,
        key="multiselect_index_name",
    )

    # Modify the df
    filtered_df = df.copy()

    # print("---------------------------------------------------------------------------")
    # print(" garment_group_name",len(filtered_df. index))

    mask = filtered_df['garment_group_name'].isin(garment_group_name_filtered_lst)
    filtered_df = filtered_df[mask]

    # print(" product_group_name",len(filtered_df. index))

    mask = filtered_df['product_group_name'].isin(product_group_name_filtered_lst)
    filtered_df = filtered_df[mask]

    # print(" index_name",len(filtered_df. index))

    mask = filtered_df['index_name'].isin(index_name_lst_filtered_lst)
    filtered_df = filtered_df[mask]

    # print(" product_code",len(filtered_df. index))

    if len(product_code_filter) > 0:
        filtered_df2 = filtered_df.loc[filtered_df["product_code"] == int(product_code_filter)]
    else:
        filtered_df2 = filtered_df

    # print(" reset_index", len(filtered_df2.index))

    filtered_df2 = filtered_df2.reset_index(drop=True)
    st.dataframe(filtered_df2, use_container_width=True)

    #####################################################################
    # ###############  KPIS  KPIS  KPIS  KPIS  KPIS  ################## #
    #####################################################################

    kpi1, kpi2, kpi3 = st.columns(3)

    kp1_value = filtered_df2["article_id"].unique()
    delta_kp1 = len(kp1_value) - len(df["article_id"].unique())
    kpi1.metric(
        label="Number unique articles",
        value=len(kp1_value),
        delta=delta_kp1,
    )

    kp2_value = filtered_df2["product_code"].unique()
    delta_kp2 = len(kp2_value) - len(df["product_code"].unique())

    kpi2.metric(
        label="Number unique product codes",
        value=len(kp2_value),
        delta=delta_kp2,
    )

    kp3_value = filtered_df2["colour_group_name"].unique()
    delta_kp3 = len(kp3_value) - len(df["colour_group_name"].unique())
    kpi3.metric(
        label="Number unique colors",
        value=len(kp3_value),
        delta=delta_kp3,
    )


    # Garment Group Graph -----------------------------------------------------------------------------------
    # Calculate count of unique garment group names
    group_counts = filtered_df2['garment_group_name'].value_counts().reset_index()
    group_counts.columns = ['garment_group_name', 'count']

    # Create a new column 'row_number' containing the row numbers
    group_counts['row_number'] = range(len(group_counts))

    # Create a new column 'color' with alternating values of 'red' and 'lightsalmon'
    group_counts['color'] = group_counts['row_number'].apply(lambda x: 'red' if x % 2 == 0 else 'lightsalmon')

    # Create an Altair chart
    chart = alt.Chart(group_counts).mark_bar().encode(
        x=alt.X('garment_group_name:N', sort="-y"),
        y='count:Q',
        color=alt.Color('color:N', scale=None, legend=None)
    )

    # Display the chart in Streamlit
    st.write("Number of articles for each Garment Group")
    st.altair_chart(chart, use_container_width=True)

    # Product Group Graph -----------------------------------------------------------------------------------
    product_counts = filtered_df2['product_group_name'].value_counts().reset_index()
    product_counts.columns = ['product_group_name', 'count']

    # Create a new column 'row_number' containing the row numbers
    product_counts['row_number'] = range(len(product_counts))

    # Create a new column 'color' with alternating values of 'red' and 'lightsalmon'
    product_counts['color'] = product_counts['row_number'].apply(lambda x: 'red' if x % 2 == 0 else 'lightsalmon')

    # Create an Altair chart
    chart = alt.Chart(product_counts).mark_bar().encode(
        x=alt.X('product_group_name:N', sort="-y"),
        y='count:Q',
        color=alt.Color('color:N', scale=None, legend=None)
    )

    # Display the chart in Streamlit
    st.write("Number of articles for each Product Group")
    st.altair_chart(chart, use_container_width=True)

    # Index Group Graph -----------------------------------------------------------------------------------
    index_name_counts = filtered_df2['index_name'].value_counts().reset_index()
    index_name_counts.columns = ['index_name', 'count']

    # Create a new column 'row_number' containing the row numbers
    index_name_counts['row_number'] = range(len(index_name_counts))

    # Create a new column 'color' with alternating values of 'red' and 'lightsalmon'
    index_name_counts['color'] = index_name_counts['row_number'].apply(lambda x: 'red' if x % 2 == 0 else 'lightsalmon')

    # Create an Altair chart
    chart = alt.Chart(index_name_counts).mark_bar().encode(
        x=alt.X('index_name:N', sort="-y"),
        y='count:Q',
        color=alt.Color('color:N', scale=None, legend=None)
    )

    # Display the chart in Streamlit
    st.write("Number of articles for each Index Name")
    st.altair_chart(chart, use_container_width=True)