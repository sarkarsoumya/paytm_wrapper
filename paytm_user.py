import requests
import json
import base64

from constants import PAYTM_ACCOUNTS_URL, PAYTM_CLIENT_ID, PAYTM_CLIENT_SECRET


class PaytmUser:

    def generate_otp(self, phone):

        url = PAYTM_ACCOUNTS_URL + '/signin/otp'
        data = dict()
        data['email'] = 'garbage@email.com'
        data['phone'] = phone
        data['clientId'] = PAYTM_CLIENT_ID
        data['scope'] = "wallet"
        data['responseType'] = "token"

        otp_response = requests.post(url, data=json.dumps(data))
        state = None

        if otp_response.status_code is 200:
            state = otp_response.json()['state']

        return state

    def generate_token(self, otp, state):
        url = PAYTM_ACCOUNTS_URL + '/signin/validate/otp'
        data = dict()
        data['otp'] = otp
        data['state'] = state
        headers = {
            'Authorization': 'Basic ' + (base64.b64encode((PAYTM_CLIENT_ID + ":" + PAYTM_CLIENT_SECRET).encode('utf-8'))).decode('utf-8')
        }
        token_response = requests.post(url, data=json.dumps(data), headers=headers)
        token = dict()

        if token_response.status_code is 200:
            token = token_response.json()

        return token

    def validate_token(self, token):
        url = PAYTM_ACCOUNTS_URL + '/user/details'
        headers = {
            'session_token' : token
        }

        user_data = dict()

        response = requests.get(url, headers=headers)
        if response.status_code is 200:
            user_data = response.json()

        return user_data
