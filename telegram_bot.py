import telebot
import subprocess
import os
from flask import Flask
from threading import Thread

TOKEN = "8285491470:AAHWHYe7um-khK-2GsC-3JedLQQBQ-D0cuc"
bot = telebot.TeleBot(TOKEN)

# Render-কে চালু রাখতে ছোট ওয়েব সার্ভার
app = Flask('')
@app.route('/')
def home(): return "Bot is Live!"
def run(): app.run(host='0.0.0.0', port=8080)

@bot.message_handler(func=lambda message: True)
def get_options(message):
    url = message.text
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("🎬 Video", callback_data=f"vid_{url}"))
    markup.add(telebot.types.InlineKeyboardButton("🎶 Audio", callback_data=f"aud_{url}"))
    bot.send_message(message.chat.id, "নিচের অপশনটি বেছে নিন:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def download(call):
    action, url = call.data.split('_', 1)
    bot.edit_message_text("⏳ প্রসেস হচ্ছে... দয়া করে অপেক্ষা করুন।", call.message.chat.id, call.message.message_id)
    
    file_name = "dl_video.mp4" if action == "vid" else "dl_audio.mp3"
    # অল্প রেজোলিউশনে ডাউনলোড করবে যাতে সার্ভার ক্রাশ না করে
    cmd = f'yt-dlp -f "best[ext=mp4][filesize<40M]" -o "{file_name}" "{url}"' if action == "vid" else f'yt-dlp -x --audio-format mp3 -o "{file_name}" "{url}"'

    try:
        subprocess.run(cmd, shell=True, check=True)
        with open(file_name, 'rb') as f:
            if action == "vid": bot.send_video(call.message.chat.id, f)
            else: bot.send_audio(call.message.chat.id, f)
        os.remove(file_name)
    except Exception as e:
        bot.send_message(call.message.chat.id, "❌ ফাইলটি অনেক বড় অথবা লিঙ্কটি কাজ করছে না।")

if __name__ == "__main__":
    Thread(target=run).start()
    bot.polling(none_stop=True)
    
