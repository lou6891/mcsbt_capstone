import requests
import extra_streamlit_components as stx
import datetime
import os
from dotenv import load_dotenv

cookie_manager = stx.CookieManager(key="verify_api_token")


def verify_api_token():
    load_dotenv()
    cookie_manager.get_all()
    auth_token = cookie_manager.get("ApiToken")
    refresh_token = cookie_manager.get("refreshToken")

    if auth_token:
        return auth_token

    elif refresh_token:
        # Send the username and hashed password to the API
        url = os.getenv("BASE_API_URL") + "api/v1/users/refresh/"

        response = requests.post(url, headers={"Authorization": "Bearer " + str(refresh_token)})

        if response.ok:
            token = response.json()["token"]
            timedelta_token = int(response.json()["token_timedelta"])
            auth_token_exp = datetime.datetime.now() + datetime.timedelta(minutes=timedelta_token)
            cookie_manager.set("ApiToken", token, expires_at=auth_token_exp, key="RegeneratingToken")
            return token
        else:
            return False
    else:
        return False
