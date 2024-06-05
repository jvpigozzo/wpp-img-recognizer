import os
from dotenv import load_dotenv
import json
import base64
import requests

load_dotenv()

# OpenAI API Key
api_key = os.getenv("OPENAI_API_KEY")


def model_pipeline(prompt: str, image_str: str):
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

    payload = {
        "model": "gpt-4-turbo",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{image_str}"},
                    },
                ],
            }
        ],
        "max_tokens": 300,
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
    ).json()["choices"][0]["message"]["content"]

    json_str = response.split("```json\n")[1].split("\n```")[0]

    json_data = json.loads(json_str)

    return json_data
