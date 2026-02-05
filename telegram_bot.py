import telebot
import subprocess
import os
from flask import Flask
from threading import Thread

# আপনার বটের টোকেন
TOKEN = "8285491470:AAHWHYe7um-khK-2GsC-3JedLQQBQ-D0cuc"
bot = telebot.TeleBot(TOKEN)

# --- Render-এর জন্য Fake Web Server ---
app = Flask('')
@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)
# ------------------------------------

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "👋 স্বাগতম! ভিডিও বা অডিওর লিঙ্ক দিন।")

@bot.message_handler(func=lambda message: True)
def get_options(message):
    url = message.text
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("🎬 Video", callback_data=f"vid_{url}"))
    markup.add(telebot.types.InlineKeyboardButton("🎶 Audio", callback_data=f"aud_{url}"))
    bot.send_message(message.chat.id, "নিচের অপশনটি বেছে নিন:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def process_download(call):
    # আপনার আগের ডাউনলোডের কোড এখানে থাকবে...
    pass

def start_bot():
    bot.polling(none_stop=True)

if __name__ == "__main__":
    # ওয়েব সার্ভার ব্যাকগ্রাউন্ডে চালানো
    t = Thread(target=run)
    t.start()
    # বট চালানো
    start_bot()
               
