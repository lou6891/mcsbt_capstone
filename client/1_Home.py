# References
# Adding pages:
# https://docs.streamlit.io/library/get-started/multipage-apps
# helpful Youtube video :
# https://www.youtube.com/watch?v=ydpoMxwWNA8


# first run will have nothing in session_state
import streamlit as st
import requests
import hashlib
from dotenv import load_dotenv
import os
import datetime
import extra_streamlit_components as stx
from utils.PageManagementModule import *

# ####### COOKIES COOKIES COOKIES ####### #

# Initialize the cookie manager
cookie_manager = stx.CookieManager()

# Set the title of the web app
st.title("Home Page")


# Define the login and registration tabs
def login_tabs(cookie_manager):
    # Create tabs for Login and Register
    tab1, tab2 = st.tabs(["Login", "Register"])

    # Load environment variables
    load_dotenv()

    # Create the login form in the Login tab
    with tab1:
        # Set subheader for the login form
        st.subheader("Login Form")

        # Input fields for username and password
        username = st.text_input("Username", key="LoginUsername").lower()
        password = st.text_input("Password", type="password", key="LoginPassword")

        # Button to trigger the login process
        if st.button("Login", use_container_width=True):
            if len(username) > 0 and len(password) > 0:
                # Hash the password using SHA256
                hashed_password = hashlib.sha256(password.encode()).hexdigest()

                # Send the username and hashed password to the API
                url = os.getenv("BASE_API_URL") + "/api/v1/users/login/"
                response = requests.get(url, json={"username": username, "password": hashed_password})

                # Check if the API response is true
                if response.ok:
                    # Store the username in the session state
                    st.session_state["LogIn"] = True
                    st.session_state["username"] = username
                    st.success("Logged in!")

                    # Set tokens and expiration times
                    auth_token = response.json()["token"]
                    timedelta_token = int(response.json()["token_timedelta"])
                    auth_token_exp = datetime.datetime.now() + datetime.timedelta(minutes=timedelta_token)

                    refresh_token = response.json()["refresh_token"]
                    timedelta_refresh = int(response.json()["refresh_token_timedelta"])
                    refresh_token_exp = datetime.datetime.now() + datetime.timedelta(days=timedelta_refresh)

                    # Set cookies
                    cookie_manager.set("AuthorizationCookie", username, expires_at=refresh_token_exp,
                                       key="AuthorizationCookie")
                    cookie_manager.set("ApiToken", auth_token, expires_at=auth_token_exp, key="ApiToken")
                    cookie_manager.set("refreshToken", refresh_token, expires_at=refresh_token_exp, key="refreshToken")

                    # Show all pages and set login state to true
                    show_all_pages()
                    st.session_state["LogIn"] = True
                else:
                    st.error("Incorrect username or password")
            else:
                st.error("Username or Password not valid")

    with tab2:
        # Create a Streamlit app
        st.subheader("Registration Form")
        st.text("Automatic login on successful registration")

        # Create the registration form with input fields for the username and password
        username = st.text_input("Username", key="RegisterUsername").lower()
        password = st.text_input("Password", type="password", key="RegisterPassword")
        confirm_password = st.text_input("Confirm Password", type="password", key="ConfirmPassword")

        # Create a button that will trigger the registration process when clicked
        if st.button("Register", use_container_width=True):
            if len(username) > 0:
                if len(password) > 0:
                    if password != confirm_password:
                        st.error("Passwords do not match")
                    else:
                        # Hash the password using SHA256
                        hashed_password = hashlib.sha256(password.encode()).hexdigest()

                        # Send the username and hashed password to the API
                        url = os.getenv("BASE_API_URL") + "api/v1/users/register/"

                        response = requests.post(url, json={"username": username, "password": hashed_password})

                        # Check if the API response is true
                        if response.ok:

                            # Store the username in the session state
                            st.session_state["LogIn"] = True
                            st.session_state["username"] = username
                            st.success("Registration successful!")

                            auth_token = response.json()["token"]
                            timedelta_token = int(response.json()["token_timedelta"])
                            auth_token_exp = datetime.datetime.now() + datetime.timedelta(minutes=timedelta_token)

                            refresh_token = response.json()["refresh_token"]
                            timedelta_refresh = int(response.json()["refresh_token_timedelta"])
                            refresh_token_exp = datetime.datetime.now() + datetime.timedelta(days=timedelta_refresh)

                            cookie_manager.set("AuthorizationCookie", username, expires_at=refresh_token_exp,
                                               key="AuthorizationCookie")
                            cookie_manager.set("ApiToken", auth_token, expires_at=auth_token_exp, key="ApiToken")
                            cookie_manager.set("refreshToken", refresh_token, expires_at=refresh_token_exp,
                                               key="refreshToken")

                            # Then go to the Home page
                            show_all_pages()
                        else:
                            st.error("Registration failed")
                else:
                    st.error("Password not valid")
            else:
                st.error("Username not valid")


# Check if there's no authorization cookie and the user is not logged in
if not cookie_manager.get("AuthorizationCookie"):
    if "LogIn" not in st.session_state:
        # Clear all pages except the first page (login/registration)
        clear_all_but_first_page()
        # Display the login and registration tabs
        login_tabs(cookie_manager)

# If the user has an authorization cookie
if cookie_manager.get("AuthorizationCookie"):
    # Show all pages in the app
    show_all_pages()

    # Create Home and Log Out tabs
    Home, LogOut = st.tabs(["Home", "Log Out"])

    # Content for the Home tab
    with Home:
        st.markdown('''
                    # Welcome to the H&M Analytics Dashboard!

                    Are you ready to explore H&M's articles, customers, and transactions? 
                    Look no further than this Streamlit app! 

                    ## Uncover Insights with Ease

                    With this tool, you can easily dive into each database's **unique page** and explore **various 
                    filters** and **KPIs**. Gain insights into H&M's performance, understand customer behavior, 
                    analyze product trends, and track transactional data, all with just a few clicks.

                    It provides an **easy-to-use interface** that allows you to filter through the data and view 
                    it in a **visually appealing** and **informative** way. 
                    You'll find charts, graphs, and tables that provide you with a comprehensive overview of each 
                    database.

                    ## Empowering Data-Driven Decisions

                    This dashboard is designed to help you uncover valuable insights that can help H&M make 
                    **data-driven decisions** for the future. By leveraging the power of data, you can stay ahead of 
                    the competition and drive success for your business.

                    Thank you for using this app, and we hope you find it useful!
                    Made by Luca Conti
                    ''')

    # Content for the Log-Out tab
    with LogOut:
        st.subheader("Thanks for stopping by! It's been great having you here! ")
        # Button to trigger the logout process
        if st.button("LogOut", use_container_width=True):
            # If the user is logged in
            if "LogIn" in st.session_state:
                # Remove the login state
                del st.session_state["LogIn"]

            # Delete the authorization, refresh, and API tokens from the cookies
            cookie_manager.delete("AuthorizationCookie", key="DeleteAuthorizationCookie")
            cookie_manager.delete("refreshToken", key="DeleteRefreshToken")
            cookie_manager.delete("ApiToken", key="DeleteApiToken")

            # Clear all pages except the first page (login/registration)
            clear_all_but_first_page()
