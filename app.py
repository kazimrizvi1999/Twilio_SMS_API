import mimetypes
from flask import Flask, Response, request
import json
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import os
from dotenv import load_dotenv
import time

app = Flask(__name__)

load_dotenv()
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')

@app.route("/sms-reply", methods=['GET', 'POST'])
def sms_reply():
    body = request.values.get('Body').lower()
    resp = MessagingResponse()
    
    if 'yes' in body:
        resp.message("You replied yes!")
    elif 'no' in body:
        resp.message("You replied no!")
    else:
        resp.message("You did not reply with yes or no")

    return Response(str(resp), mimetype="application/xml")

@app.route("/sms-send", methods=['GET', 'POST'])
def sms_send():
    if request.method == 'GET':
        return {"data": [account_sid, auth_token]}

    byte_data = request.data
    data = byte_data.decode('utf-8').replace("'", '"')
    json_data = json.loads(data)

    numbers = json_data['numbers']
    sender = json_data['sender']
    message_body = json_data['message_body']
    
    client = Client(account_sid, auth_token)

    for number in numbers:
        message = client.messages \
        .create(
            body=message_body,
            from_=sender,
            to=number
        )
        print(message.sid)
    return {"status": 200}

if __name__ == "__main__":
    app.run()
