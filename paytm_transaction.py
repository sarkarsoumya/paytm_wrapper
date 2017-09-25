import requests
import json
from collections import OrderedDict
import urllib.parse

from checksum import generate_checksum
from constants import PAYTM_BALANCE_URL, PAYTM_MID, PAYTM_INDUSTRY_TYPE, PAYTM_CHANNEL_ID, PAYTM_MERCHANT_KEY


class PaytmTransaction:

    def check_balance(self, token):
        wallet_url = PAYTM_BALANCE_URL
        data = dict()
        data['request'] = dict()
        data['request']['mid'] = PAYTM_MID

        headers = {
            "ssotoken": token
        }

        balance = dict()

        response = requests.post(wallet_url, data=json.dumps(data), headers=headers)
        if response.status_code is 200:
            balance = response.json()

        return balance

    def withdraw(self, order_id, amount, phone, token,customer_id, channel=PAYTM_CHANNEL_ID, currency="INR"):
        data = {
            "OrderId": order_id,
            "ReqType": "WITHDRAW",
            "MID": PAYTM_MID,
            "AppIP": "127.0.0.1",
            "TxnAmount": amount,
            "Currency": currency,
            "DeviceId": phone,
            "SSOToken": token,
            "PaymentMode": "PPI",
            "CustId": customer_id,
            "IndustryType": PAYTM_INDUSTRY_TYPE,
            "Channel": channel,
            "AuthMode": "USRPWD",
        }
        data['CheckSum'] = urllib.parse.quote(generate_checksum(data, PAYTM_MERCHANT_KEY).decode('utf-8'))

        data_string = 'JsonData=' + json.dumps(data)
        withdraw_url = 'https://pguat.paytm.com/oltp/HANDLER_FF/withdrawScw'
        headers = {
            'Content-Type': 'application/json'
        }

        transaction_data = dict()

        response = requests.post(withdraw_url, data=data_string, headers=headers)
        if response.status_code is 200:
            transaction_data = response.json()

        return transaction_data
