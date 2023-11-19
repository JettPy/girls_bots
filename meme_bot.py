import os
import dotenv
import telebot


dotenv.load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

bot.infinity_polling()
