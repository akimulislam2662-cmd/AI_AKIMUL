import os
import asyncio
import google.generativeai as genai
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import threading

# আপনার তথ্য
BOT_TOKEN = "8353282406:AAERrPZZXnIKNP650fPwmbnWHthucEE4VHw"
GEMINI_KEY = "AIzaSyAePvBRMoE0Cel4SgQcjpL0ZuOUYwtH058"

genai.configure(api_key=GEMINI_KEY)
ai_model = genai.GenerativeModel('gemini-1.5-flash')

app = Flask('')

@app.route('/')
def home():
    return "Bot is Online!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        try:
            response = ai_model.generate_content(update.message.text)
            await update.message.reply_text(response.text)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    # Flask সার্ভার আলাদাভাবে চালানো
    t = threading.Thread(target=run_flask)
    t.daemon = True
    t.start()

    # টেলিগ্রাম বট সেটআপ
    app_bot = ApplicationBuilder().token(BOT_TOKEN).build()
    app_bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Render এর লুপ সমস্যা এড়াতে এটি সবচেয়ে নিরাপদ পদ্ধতি
    print("Starting bot...")
    app_bot.run_polling(drop_pending_updates=True)
