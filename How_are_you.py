import telebot
import os
import dotenv

dotenv.load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")
bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.from_user.id, "Привет, как вас зовут")
    bot.register_next_step_handler(message, get_name)


def get_name(message):
   name = message.text
   bot.send_message(message.from_user.id, F"Cпасибо,{name}!")


bot.infinity_polling()