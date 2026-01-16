import os
import threading
import asyncio
import base64
import requests
import google.generativeai as genai
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# সরাসরি টোকেনগুলো সেট করা হলো
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

async def run_bot():
    # এই অংশটি আপনার Event Loop সমস্যা সমাধান করবে
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    async with application:
        await application.initialize()
        await application.start_polling()
        await asyncio.Event().wait()

if __name__ == '__main__':
    # Flask সার্ভার চালু করা
    threading.Thread(target=run_flask, daemon=True).start()
    
    # বট রান করা
    try:
        asyncio.run(run_bot())
    except RuntimeError:
        # যদি লুপ অলরেডি চলতে থাকে তবে এটি ব্যবহার করবে
        loop = asyncio.get_event_loop()
        loop.create_task(run_bot())
