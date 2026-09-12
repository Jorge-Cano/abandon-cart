import functions_framework
from flask import jsonify
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

# Hardcoded or retrieved credentials
TWILIO_ACCOUNT_SID = "YOUR_UNIQUE_SID"
TWILIO_AUTH_TOKEN = "YOUR_UNIQUE_TOKEN"
TWILIO_PHONE_NUMBER = "YOUR_TWILIO_PHONE"


@functions_framework.http
def send_sms_endpoint(request):
    """
    HTTP Cloud Function to process POST requests and send SMS via Twilio.
    
    Expected Entry Point in Cloud Console: send_sms_endpoint
    Expected JSON Payload:
    {
        "phone_number": "+12105550199",
        "message": "Notification payload from application"
    }
    """
    # 1. Enforce POST HTTP method
    if request.method != "POST":
        return jsonify({"status": "error", "message": "Method Not Allowed. Use POST."}), 405

    # 2. Extract and parse JSON body
    request_json = request.get_json(silent=True)
    if not request_json:
        return jsonify({"status": "error", "message": "Invalid or missing JSON payload."}), 400

    recipient_phone = request_json.get("phone_number")
    message_body = request_json.get("message")

    if not recipient_phone or not message_body:
        return jsonify({
            "status": "error",
            "message": "Missing required fields: 'phone_number' and 'message'."
        }), 422

    # 3. Instantiate Twilio Client and send message
    # Client initialization is placed inside the request handler so import/credential
    # errors return an HTTP error rather than crashing container boot on port 8080.
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        
        sent_message = client.messages.create(
            body=message_body,
            from_=TWILIO_PHONE_NUMBER,
            to=recipient_phone
        )
        
        return jsonify({
            "status": "success",
            "sid": sent_message.sid,
            "recipient": recipient_phone
        }), 200

    except TwilioRestException as e:
        return jsonify({"status": "error", "detail": f"Twilio API Error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"status": "error", "detail": f"Unexpected error: {str(e)}"}), 500
