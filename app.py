import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
import requests
from twilio.twiml.messaging_response import MessagingResponse

from utils import encode_image, send_message
from model import model_pipeline

load_dotenv()

twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID")
twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")

app = Flask(__name__)


@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    form = request.form
    media_url = form.get("MediaUrl0")

    if media_url:
        r = requests.get(
            media_url, stream=True, auth=(twilio_account_sid, twilio_auth_token)
        )
        image_data = r.content
        image_str = encode_image(image_data)
        model_result = model_pipeline(
            prompt="How much does gas cost? Return data as JSON {price: float, advertiser: str}",
            image_str=image_str,
        )
        if model_result:
            print('ALOHAAAA')
            send_message(
                f"Obrigado! Recebemos a sua foto! Os dados são {model_result}"
            )
            return jsonify({"message":"Flask"})
        else:
            print('ALOHAAAA')
            send_message("Por favor, envie uma imagem!")
            return jsonify({"message":"Flask"})
    else:
        send_message("Por favor, envie uma imagem!")
        return jsonify({"message":"Flask"})


if __name__ == "__main__":
    app.run(debug=True)
