import os
import json
import base64
import random

import random
from datetime import datetime, timedelta


from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from dotenv import load_dotenv

load_dotenv()

twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID")
twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")


def encode_image(content):
    return base64.b64encode(content).decode("utf-8")


def send_message(body_text):
    client = Client(twilio_account_sid, twilio_auth_token)
    message = client.messages.create(
        from_="whatsapp:+14155238886", body=body_text, to="whatsapp:+5521981483435"
    )
    message_sid = message.sid
    message_sent = client.messages(message_sid).fetch()
    if message_sent.status == "failed":
        print("Error Code:", message_sent.error_code)
        print("Error Message:", message_sent.error_message)
