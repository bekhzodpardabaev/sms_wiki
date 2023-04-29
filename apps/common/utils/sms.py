from config.settings import (
    SMS_PROVIDER,
    ESKIZ_API_TOKEN,
    ESKIZ_EMAIL,
    ESKIZ_PASSWORD,
    PLAY_MOBILE_LOGIN,
    PLAY_MOBILE_PASSWORD,
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
    TWILIO_PHONE_NUMBER,
)

from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

import logging
import requests


# ESKIZ
class Eskiz:

    @classmethod
    def _login(cls, email, password):
        if not email or not password:
            return ""
        url = "https://notify.eskiz.uz/api/auth/login"
        payload = """{
            "email": "%s",
            "password": "%s"
        }""" % (email, password)
        headers = {
            'content-type': "application/json",
        }
        response = requests.request("POST", url, data=payload, headers=headers)
        try:
            return response.json()['data']['token']
        except KeyError as e:
            logging.error(str(e))
            logging.error(str(response.text))
            return ""

    @classmethod
    def _get_bearer_token(cls):
        url = "http://notify.eskiz.uz/api/auth/user"
        headers = {
            'authorization': f"Bearer {ESKIZ_API_TOKEN}",
        }
        response = requests.request("GET", url, headers=headers)
        if response.status_code == 200:
            return ESKIZ_API_TOKEN
        return cls._login(ESKIZ_EMAIL, ESKIZ_PASSWORD)

    @classmethod
    def eskiz_send_sms(cls, phone_number, message):
        """
        {
            "mobile_phone": "998912345678",
            "message": "Test sms",
            "from": "4546"
        }
        """
        phone_number = phone_number.replace("+", "")
        bearer_token = cls._get_bearer_token()
        url = "http://notify.eskiz.uz/api/message/sms/send"

        payload = """{
            "mobile_phone": "%s", 
            "message": "%s",
            "from": "4546"
        }""" % (phone_number, message)
        headers = {
            'authorization': f"Bearer {bearer_token}",
            'content-type': "application/json",
        }
        response = requests.request("POST", url, data=payload, headers=headers, timeout=5)

        if response.status_code != 200:
            logging.error(str(response.text))


# TWILIO
def send_via_twilio(phone_number, message):
    """
        {
            to="+15558675310",
            body="Hey there!",
            from_="+15017122661"
        }
    """

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    # LOGGING
    logging.basicConfig(filename='./log.txt')
    client.http_client.logger.setLevel(logging.INFO)

    try:
        message = client.messages.create(
            to=phone_number,
            from_=TWILIO_PHONE_NUMBER,
            body=message,
        )
        return message.sid
    except TwilioRestException as e:
        # Implement your fallback code
        print(e)


# PLAYMOBILE
def play_mobile_send_sms(phone_number, message):
    url = "http://91.204.239.44/broker-api/send"
    phone_number = phone_number.replace("+", "")
    response = requests.post(
        url,
        auth=(PLAY_MOBILE_LOGIN, PLAY_MOBILE_PASSWORD),
        json={
            "messages": [
                {
                    "recipient": str(phone_number),
                    "message-id": "1",
                    "sms": {
                        "originator": "3700",
                        "content": {
                            "text": message},
                    },
                }
            ]
        },
        timeout=5
    )
    return response


def send_sms(phone_number, message):
    if SMS_PROVIDER == 'twilio':
        return send_via_twilio(phone_number, message)
    elif SMS_PROVIDER == 'eskiz':
        return Eskiz.eskiz_send_sms(phone_number, message)
    elif SMS_PROVIDER == 'playmobile':
        return play_mobile_send_sms(phone_number, message)
    else:
        raise Exception('Unknown sms provider')
