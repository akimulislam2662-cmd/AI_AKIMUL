import os
import threading
import asyncio
import base64
import requests
import google.generativeai as genai
from flask import Flask
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# আপনার টোকেনগুলো (এগুলো কোডেই থাকবে, তাই Render এর ভেরিয়েবল নিয়ে টেনশন নেই)
BOT_TOKEN = "8353282406:AAERrPZZXnIKNP650fPwmbnWHthucEE4VHw"
GEMINI_KEY = "AIzaSyAePvBRMoE0Cel4SgQcjpL0ZuOUYwtH058"
GITHUB_TOKEN = "Ghp_IoZlGcr3WyzWJbAk4kbJJoUeI7WZgh083EHY"
REPO_NAME = "akimulislam2662-cmd/AI_AKIMUL"

genai.configure(api_key=GEMINI_KEY)
ai_model = genai.GenerativeModel('gemini-1.5-flash')

app = Flask('')

@app.route('/')
def home():
    return "Bot is active and running!"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        try:
            response = ai_model.generate_content(update.message.text)
            await update.message.reply_text(response.text)
        except Exception as e:
            print(f"Error: {e}")

def run_flask():
    # Render এর জন্য নির্দিষ্ট পোর্ট (10000)
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def main():
    # Flask কে আলাদাভাবে চালানো
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # টেলিগ্রাম বট সেটআপ (সহজ পদ্ধতিতে)
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # পোলিং শুরু
    application.run_polling(close_loop=False)

if __name__ == '__main__':
    main()
