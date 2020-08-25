import requests
from requests.auth import HTTPBasicAuth

import mpesa.keys as keys


def generate_access_token():

    consumer_key = keys.consumer_key
    consumer_secret = keys.consumer_secret
    api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    try:
        r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
        print(r)
    except Exception as e:
        print(f'Error from exception is:{e}')
        r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret), verify=False)
        
    print(r.text)

    json_response = (
        r.json()
    )  # {'access_token': 'orfE9Dun2qqCpuXsORjcWGzvrAIY', 'expires_in': '3599'}

    my_access_token = json_response["access_token"]

    return my_access_token


#generate_access_token()