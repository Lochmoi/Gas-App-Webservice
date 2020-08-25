import requests
from requests.auth import HTTPBasicAuth
from mpesa.access_token import generate_access_token
from mpesa.encode import generate_password
from mpesa.utils import get_timestamp, change_phone_no_format
import mpesa.keys as keys


def lipa_na_mpesa(phone_no, amount):
    formatted_time = get_timestamp()
    print(formatted_time)
    decoded_password = generate_password(formatted_time)
    print(decoded_password)
    access_token = generate_access_token()
    print(access_token)

    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

    headers = {"Authorization": "Bearer %s" % access_token}

    request = {
        "BusinessShortCode": keys.business_shortCode,
        "Password": decoded_password,
        "Timestamp": formatted_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": change_phone_no_format(phone_no),
        "PartyB": keys.business_shortCode,
        "PhoneNumber": change_phone_no_format(phone_no),
        "CallBackURL": "https://mysterious-oasis-16355.herokuapp.com/api/payments/lnm/",
        "AccountReference": "test aware",
        "TransactionDesc": "Pay for gas",
    }

    response = requests.post(api_url, json=request, headers=headers)

    print(response.text)


#lipa_na_mpesa()