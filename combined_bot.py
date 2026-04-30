from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import asyncio
import threading

# ====== CONFIG ======
TELEGRAM_TOKEN = "8713103184:AAFeJrQNpfJB9hqmSDJBaRgT67odOIVsFL8"

# ====== FAQ DATA ======
FAQS = {
    "bet settlement": "We will check the bet details and get back to you shortly.",
    "transaction": "We will review the transaction details and update you shortly.",
    "game issue": "We are checking the issue with the provider and will update you soon.",
    "game launch": "We will check the game launch issue and update you shortly.",
    "results": "We will verify and share the results shortly.",
    "whitelist": "We will whitelist the domains and update you shortly.",
    "balance": "Please refresh your account or log in again.",
    "deposit": "Please check with your payment provider.",
    "withdraw": "Your withdrawal is under process.",
    "login": "Please try clearing cache and logging in again.",
    "network": "We are checking the network issue.",
    "maintenance": "We are currently under maintenance."
}

# ====== COMMON LOGIC ======
def get_reply(text):
    text = text.lower()
    for keyword in sorted(FAQS.keys(), key=len, reverse=True):
        if keyword in text:
            return FAQS[keyword]
    return "Our support team will assist you shortly."

# ====== TELEGRAM ======
async def telegram_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    response = get_reply(update.message.text)
    await update.message.reply_text(response)

def run_telegram():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT, telegram_reply))
    print("Telegram bot running...")
    app.run_polling()

# ====== WHATSAPP (Flask) ======
flask_app = Flask(__name__)

@flask_app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    incoming_msg = request.form.get('Body', '')
    reply = get_reply(incoming_msg)
    resp = MessagingResponse()
    resp.message(reply)
    return str(resp)

def run_flask():
    print("WhatsApp bot running on port 5000...")
    flask_app.run(port=5000)

# ====== MAIN ======
if __name__ == "__main__":
    t1 = threading.Thread(target=run_telegram)
    t1.start()

    run_flask()