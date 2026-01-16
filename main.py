import os
import threading
import asyncio
import base64
import requests
import google.generativeai as genai
from flask import Flask
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# Render এর Environment Variables থেকে টোকেনগুলো নেওয়া হচ্ছে
BOT_TOKEN = os.environ.get("BOT_TOKEN")
GEMINI_KEY = os.environ.get("GEMINI_KEY")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
REPO_NAME = "akimulislam2662-cmd/AI_AKIMUL"

genai.configure(api_key=GEMINI_KEY)
ai_model = genai.GenerativeModel('gemini-1.5-flash')

app = Flask('')
@app.route('/')
def home(): return "Rupali AI is Running"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

# GitHub এ কোড অটো-আপডেট করার ফাংশন
def update_github_file(new_code):
    url = f"https://api.github.com/repos/{REPO_NAME}/contents/main.py"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    res = requests.get(url, headers=headers).json()
    sha = res['sha']
    content = base64.b64encode(new_code.encode()).decode()
    data = {"message": "Auto-update from Bot", "content": content, "sha": sha}
    requests.put(url, headers=headers, json=data)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    # ফিচার যোগ করার কমান্ড চেক
    if "যোগ করো" in user_text:
        await update.message.reply_text("একটু সময় দাও জান, আমি নতুন ফিচারটি আমার ব্রেইনে যোগ করছি...")
        prompt = f"Provide the full updated python code for this telegram bot including: {user_text}. Output only code."
        response = ai_model.generate_content(prompt)
        new_code = response.text.replace("```python", "").replace("```", "").strip()
        update_github_file(new_code)
        await update.message.reply_text("সফলভাবে আপডেট করেছি! এখন আমি রিস্টার্ট নিচ্ছি।")
    else:
        # সাধারণ এআই চ্যাট
        response = ai_model.generate_content(user_text)
        await update.message.reply_text(response.text)

async def main():
    threading.Thread(target=run_flask).start()
    bot = Application.builder().token(BOT_TOKEN).build()
    bot.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    await bot.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
