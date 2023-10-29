import telebot
import os
import dotenv

dotenv.load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")
bot = telebot.TeleBot(API_TOKEN)

inline_menu = telebot.types.InlineKeyboardMarkup()
btn_1 = telebot.types
# cities = ("Нью - Йорк", "Москва", "Санкт - Петербург", "")


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.from_user.id, ",бот запустился")
    pass

@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.from_user.id, "нужна помощь?")

bot.infinity_polling()
