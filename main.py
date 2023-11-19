import telebot
import os
import dotenv

dotenv.load_dotenv()
API_TOKEN = os.getenv('API-TOKEN')
bot = telebot.TeleBot('6066709389:AAGGnZBVA6-zqGaH1JOjUjJOLXWRWLTIDLQ')


@bot.message_handler(content_types=['text'])
def text(massage):
    bot.reply_to(massage, massage.text)


bot.infinity_polling()