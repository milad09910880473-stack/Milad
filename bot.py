bot.py
import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import yt_dlp

BOT_TOKEN = "8924509328:AAGJEBa4DDbydq-qYooSugiP5F1jKqD-q58"
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🎧 ربات قفل‌موزیک (GHOFL.M) آماده به کار است!\nاسم آهنگ یا خواننده رو بفرست برام:")

@bot.message_handler(func=lambda message: True)
def search_and_download(message):
    query = message.text.strip()
    status_msg = bot.reply_to(message, "🔎 در حال قفل روی موزیک و دانلود...")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
        'noplaylist': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch1:{query}", download=True)
            if 'entries' in info and len(info['entries']) > 0:
                entry = info['entries'][0]
                filename = ydl.prepare_filename(entry)
                audio_file = os.path.splitext(filename)[0] + ".mp3"
                title = entry.get('title', query)
                performer = entry.get('uploader', 'GHOFL.M')

                markup = InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton("📢 کانال ما", url="https://t.me/GhoflMusicBot"))

                with open(audio_file, 'rb') as audio:
                    bot.send_audio(
                        message.chat.id,
                        audio,
                        title=title,
                        performer=performer,
                        caption=f"🎵 {title}\n\n🔒 @GhoflMusicBot | قفل‌موزیک",
                        reply_markup=markup
                    )
                
                if os.path.exists(audio_file):
                    os.remove(audio_file)
                bot.delete_message(message.chat.id, status_msg.message_id)
            else:
                bot.edit_message_text("❌ متأسفانه آهنگی پیدا نشد.", message.chat.id, status_msg.message_id)
    except Exception as e:
        bot.edit_message_text("⚠️ خطایی در دانلود پیش آمد.", message.chat.id, status_msg.message_id)

if __name__ == '__main__':
    print("Bot is running...")
    bot.infinity_polling()

