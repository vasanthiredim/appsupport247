from flask import Flask, request
import requests
import os

app = Flask(__name__)

# Telegram Bot Token
TOKEN = "8783576920:AAHMBSnxlOp9BFka45fiJBC6nlT_WPOQfsM"

# FAQ Responses
FAQS = {
    "bet settlement": "Thank you for reaching out. We will check the bet details and get back to you shortly.",
    "transaction": "We will review the transaction details and update you shortly.",
    "game launch": "We will check the game launch issue with the provider and update you shortly.",
    "results": "We will verify and share the results shortly.",
    "whitelist": "We will whitelist the domains and update you shortly.",
    "balance": "Please refresh your account or log in again to check the updated balance.",
    "deposit": "Please check with your payment provider.",
    "withdraw": "Your withdrawal is under process. Please allow some time.",
    "login": "Please try clearing your cache and logging in again.",
    "maintenance": "We are currently under maintenance. Services will resume shortly.",
    "new provider": "We will check with our team and enable the requested provider.",
    "game list": "We will review the game list and update you shortly.",
    "network error": "We are checking the network issue and will update you shortly.",
    "callback": "We will update the callback URL and confirm shortly.",
    "currency": "We will review and enable the requested currency.",
    "integration": "We are working on the setup and will share the credentials once completed."
}

# Function to get matching reply
def get_reply(text):
    text = text.lower()

    for keyword in sorted(FAQS.keys(), key=len, reverse=True):
        if keyword in text:
            return FAQS[keyword]

    return "Thank you for your message. Our support team will assist you shortly."


# ==========================================
# TELEGRAM WEBHOOK
# ==========================================
@app.route("/", methods=["GET", "POST"])
def telegram_webhook():

    # Browser test
    if request.method == "GET":
        return "Bot is running"

    # Telegram webhook data
    data = request.get_json(force=True)

    print("Incoming Telegram:", data)

    message = data.get("message") or data.get("edited_message")

    if message:
        chat_id = message["chat"]["id"]
        text = message.get("text", "")

        if text:
            reply = get_reply(text)

            telegram_url = f"https://api.telegram.org/bot8783576920:AAHMBSnxlOp9BFka45fiJBC6nlT_WPOQfsM/sendMessage"

            requests.post(
                telegram_url,
                json={
                    "chat_id": chat_id,
                    "text": reply
                }
            )

    return "ok"


# ==========================================
# WHATSAPP WEBHOOK (TWILIO)
# ==========================================
@app.route("/whatsapp", methods=["POST"])
def whatsapp():

    incoming = request.form.get("Body", "")

    print("Incoming WhatsApp:", incoming)

    reply = get_reply(incoming)

    return f"""
<Response>
    <Message>{reply}</Message>
</Response>
"""

# ==========================================
# RUN APP
# ==========================================
if __name__ == "__main__":

    port = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port
    )
