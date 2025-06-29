from flask import Flask, request
from twilio.rest import Client

app = Flask(__name__)
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_FROM = os.getenv("TWILIO_FROM")

client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

@app.route('/lead-mql', methods=['POST'])
def handle_mql_lead():
    data = request.json

    name = data.get('full_name')
    mobile = data.get('mobile') 
    industry = data.get('industry')


    if not mobile or not name:
        return {"error": "Missing fields"}, 400

    message = f"Hi {name}, check out BrewSync's espresso packs made for cafés like yours! ☕"

    # Send WhatsApp (change 'whatsapp:' to '' for SMS)
    try:
        msg = client.messages.create(
            body=message,
            from_=TWILIO_FROM,
            to=f"whatsapp:{mobile}"
        )
        return {"status": "Message sent", "sid": msg.sid}, 200
    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == '__main__':
    app.run(debug=True)
