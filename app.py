from flask import Flask, Response, request
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import os
from dotenv import load_dotenv
import multiprocessing
from utils import *

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
        return {"message:" "Use post request to send sms"}

    elif request.method == 'POST':
        json_data = preprocess_data(request.data)

        numbers = json_data['numbers']
        sender = json_data['sender']
        message_body = json_data['message_body']

        numbers = split_numbers(numbers, num_threads=5)
        client = Client(account_sid, auth_token)

        processes = []

        for i, chunk in enumerate(numbers):
            p = multiprocessing.Process(
                target=launch_sms,
                args=(
                    client,
                    chunk,
                    message_body,
                    sender,
                    i+1
                )
            )
            processes.append(p)
        
        print(f"Total Processes: {len(processes)}")
        for process in processes:
            process.start()
        
        for process in processes:
            process.join()

        print("ALL MESSAGES SENT!")        
        return {"status": 200}


if __name__ == "__main__":
    app.run()