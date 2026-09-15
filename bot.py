import telebot
import os

# توکن ربات شما
TOKEN = '8924509328:AAGJEBa4DDbydq-qYooSugiP5F1jKqD-q58'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "سلام آق میلاد! ربات قفل‌موزیک با قدرت آنلاین شد! 🚀")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "آق میلاد، دستورت رو گرفتم، ولی فعلاً دارم تنظیم می‌شم. به زودی موزیک‌ها رو برات میارم! 🎵")

if __name__ == "__main__":
    bot.infinity_polling()
