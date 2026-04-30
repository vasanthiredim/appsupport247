from flask import Flask, request
import requests
import os

app = Flask(__name__)

TOKEN = os.getenv("8713103184:AAFeJrQNpfJB9hqmSDJBaRgT67odOIVsFL8")

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
    "maintenance": "We are currently under maintenance. Services will resume shortly."
}

def get_reply(text):
    text = text.lower()
    for keyword in FAQS:
        if keyword in text:
            return FAQS[keyword]
    return "Thank you for your message. Our team will assist you shortly."

# Telegram Webhook
@app.route(f"/{TOKEN}", methods=["POST"])
def telegram_webhook():
    data = request.json

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        reply = get_reply(text)

        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            json={"chat_id": chat_id, "text": reply}
        )

    return "ok"

# WhatsApp Webhook (Twilio)
@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    incoming = request.form.get("Body", "")
    reply = get_reply(incoming)
    return f"<Response><Message>{reply}</Message></Response>"

# REQUIRED for Render
@app.route("/")
def home():
    return "Bot is running"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
