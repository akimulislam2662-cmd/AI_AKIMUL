import telebot
import subprocess
import os

TOKEN = "8285491470:AAHWHYe7um-khK-2GsC-3JedLQQBQ-D0cuc"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "👋 লিঙ্ক দিন! অডিও বা ভিডিও অপশন আসবে।")

@bot.message_handler(func=lambda message: True)
def get_options(message):
    url = message.text
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("🎬 Video", callback_data=f"vid_{url}"))
    markup.add(telebot.types.InlineKeyboardButton("🎶 Audio", callback_data=f"aud_{url}"))
    bot.send_message(message.chat.id, "আপনি কী ডাউনলোড করতে চান?", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def download(call):
    action, url = call.data.split('_', 1)
    bot.edit_message_text("⏳ ডাউনলোড শুরু হচ্ছে...", call.message.chat.id, call.message.message_id)
    
    file = "video.mp4" if action == "vid" else "audio.mp3"
    cmd = f'yt-dlp -o "{file}" "{url}"' if action == "vid" else f'yt-dlp -x --audio-format mp3 -o "{file}" "{url}"'

    try:
        subprocess.run(cmd, shell=True)
        with open(file, 'rb') as f:
            if action == "vid": bot.send_video(call.message.chat.id, f)
            else: bot.send_audio(call.message.chat.id, f)
        os.remove(file)
    except Exception:
        bot.send_message(call.message.chat.id, "❌ এরর হয়েছে!")

bot.polling()
  
