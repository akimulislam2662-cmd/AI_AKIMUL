import os
import threading
import asyncio
import base64
import requests
import google.generativeai as genai
from flask import Flask
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# সরাসরি টোকেন (Render Settings এ এগুলো থাকলে কোড আরও নিরাপদ হয়)
BOT_TOKEN = "8353282406:AAERrPZZXnIKNP650fPwmbnWHthucEE4VHw"
GEMINI_KEY = "AIzaSyAePvBRMoE0Cel4SgQcjpL0ZuOUYwtH058"
GITHUB_TOKEN = "Ghp_IoZlGcr3WyzWJbAk4kbJJoUeI7WZgh083EHY"
REPO_NAME = "akimulislam2662-cmd/AI_AKIMUL"

genai.configure(api_key=GEMINI_KEY)
ai_model = genai.GenerativeModel('gemini-1.5-flash')

app = Flask('')

@app.route('/')
def home():
    return "Rupali AI is Online!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    user_text = update.message.text
    try:
        response = ai_model.generate_content(user_text)
        await update.message.reply_text(response.text)
    except Exception as e:
        print(f"Error: {e}")

def main():
    # Flask সার্ভার আলাদা থ্রেডে চালানো
    threading.Thread(target=run_flask, daemon=True).start()

    # টেলিগ্রাম বট সেটআপ
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Bot is starting...")
    application.run_polling()

if __name__ == '__main__':
    main()
