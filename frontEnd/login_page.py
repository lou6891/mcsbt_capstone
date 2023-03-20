import streamlit as st
import requests
import hashlib
from dotenv import load_dotenv
import os
import datetime
from utils.PageManagementModule import *
from streamlit_extras.switch_page_button import switch_page
import streamlit as st


def login_tabs(cookie_manager_2):
    tab1, tab2 = st.tabs(["Login", "Register"])
    # Load dotenv variables
    load_dotenv()

    with tab1:
        # Create a Streamlit app
        st.title("Login Form")

        # Create the login form with input fields for the username and password
        username = st.text_input("Username", key="LoginUsername").lower()
        password = st.text_input("Password", type="password", key="LoginPassword")

        # Create a checkbox for the "Remember me" option
        remember_me = st.checkbox("Remember me", key="LoginRememberMe")

        # Create a button that will trigger the login process when clicked
        if st.button("Login"):
            # Hash the password using SHA256
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            # Send the username and hashed password to the API
            url = os.getenv("BASE_API_URL") + "/api/v1/users/login/"
            response = requests.get(url, json={"username": username, "password": hashed_password})

            # Check if the API response is true
            # response.ok means is TRUE for all 2xx codes
            if response.ok:
                # Store the username in the session state
                st.session_state["loggedIn"] = True
                st.session_state["username"] = username
                st.success("Logged in!")

                # Set a cookie if the "Remember me" option is checked
                if remember_me:
                    expires_at = datetime.datetime.now() + datetime.timedelta(days=30)
                    cookie_manager_2.set("3", "3", expires_at=expires_at, key="abc")

            else:
                st.error("Incorrect username or password")

    with tab2:
        # Create a Streamlit app
        st.title("Registration Form")
        st.text("Automatic login on successful registration")

        # Create the registration form with input fields for the username and password
        username = st.text_input("Username", key="RegisterUsername").lower()
        password = st.text_input("Password", type="password", key="RegisterPassword")
        confirm_password = st.text_input("Confirm Password", type="password", key="ConfirmPassword")

        # Create a checkbox for the "Remember me" option
        remember_me = st.checkbox("Remember me", key="RegisterRememberMe")

        # Create a button that will trigger the registration process when clicked
        if st.button("Register"):
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
                    st.session_state["username"] = username
                    st.success("Registration successful!")

                    # Set a cookie if the "Remember me" option is checked
                    if remember_me:
                        expires_at = datetime.datetime.now() + datetime.timedelta(days=30)
                        cookie_manager_2.set("loggedInCookie", "username", expires_at=expires_at)

                    # Then go to the Home page
                    show_all_pages()
                    switch_page(SECOND_PAGE_NAME)
                else:
                    st.error("Registration failed")


def logout_tab(cookie_manager_2):
    st.write("Logout Page")
    if st.button("LogOut"):
        cookie_manager_2.delete("AuthoriazationCookie")
        clear_all_but_first_page()


def show_login_page(cookie_manager_2):
    login_tabs(cookie_manager_2)
    if cookie_manager_2.get("AuthoriazationCookie"):
        # Then go to the Home page
        show_all_pages()
        switch_page(SECOND_PAGE_NAME)


'''
    if 'loggedIn' not in st.session_state:
        clear_all_but_first_page()
        st.session_state['loggedIn'] = False
        login_tabs(cookie_manager_2)

    else:
        if st.session_state['loggedIn'] or cookie_manager_2.get("loggedInCookie"):
            st.write( cookie_manager_2.get("loggedInCookie"))
            st.write( cookie_manager_2.get_all())

            logout_tab(cookie_manager_2)
            st.write("hello")
            # switch_page(SECOND_PAGE_NAME)
            # switch to second page

        else:
            clear_all_but_first_page()
            login_tabs(cookie_manager_2)
            '''
