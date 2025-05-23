#!/usr/bin/env python3
import requests
import sys

TOKEN = "BOT_TOKEN"
CHAT_ID = sys.argv[1]
SUBJECT = sys.argv[2]
MESSAGE = sys.argv[3]

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
data = {"chat_id": CHAT_ID, "text": f"{SUBJECT}\n{MESSAGE}"}

response = requests.post(url, data=data)
print(response.json())
