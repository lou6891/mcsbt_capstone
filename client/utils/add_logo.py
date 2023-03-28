import streamlit as st


def add_logo(b_width, b_height):
    st.markdown("""
                <style>
                    [data-testid="stSidebarNav"] {{
                        background-image: url(https://upload.wikimedia.org/wikipedia/commons/5/53/H%26M-Logo.svg);
                        background-size: {}px {}px;
                        background-repeat: no-repeat;
                        padding-top: 120px;
                        background-position: 15px 30px;
                    }}
                </style>""".format(b_width, b_height),
                unsafe_allow_html=True)
