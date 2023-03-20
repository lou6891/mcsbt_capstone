import streamlit as st
import requests
import extra_streamlit_components as stx
import os
from dotenv import load_dotenv
import pandas as pd

from utils.verify_api_token import verify_api_token

load_dotenv()
df = None
cookie_manager = stx.CookieManager(key="Article_page")
st.title("Articles Dashboard")


def convert_object_to_string(df):
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].astype(str)

    return df


# API Call, first verify that the token is valid, if not get a new one, if not re login

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
        st.write("errror token validity")


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
        label="Garment Group",
        options=garment_group_name_lst,
        default=garment_group_name_lst,
        key="multiselect_garment_group_name",
    )

    # colour_group_name_lst filter
    product_group_name_lst = df["product_group_name"].unique()
    product_group_name_filtered_lst = st.sidebar.multiselect(
        label="Product Group",
        options=product_group_name_lst,
        default=product_group_name_lst,
        key="multiselect_product_group_name",
    )

    # colour_group_name_lst filter
    index_name_lst = df["index_name"].unique()

    index_name_lst_filtered_lst = st.sidebar.multiselect(
        label="index_name",
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
    kpi1.metric(
        label="Number unique articles",
        value=len(kp1_value),
        delta=len(kp1_value),
    )

    kp2_value = filtered_df2["product_code"].unique()
    kpi2.metric(
        label="Number unique product codes",
        value=len(kp2_value),
        delta=len(kp2_value),
    )

    kp3_value = filtered_df2["colour_group_name"].unique()
    kpi3.metric(
        label="Number unique colors",
        value=len(kp3_value),
        delta=len(kp3_value),
    )

    st.write("Number of articles for each Garment Group")
    st.bar_chart(filtered_df2['garment_group_name'].value_counts())
    st.write("Number of articles for each Product Group")
    st.bar_chart(filtered_df2['product_group_name'].value_counts())
    st.write("Number of articles for each Index Name")
    st.bar_chart(filtered_df2['index_name'].value_counts())
