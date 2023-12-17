import telebot
import dotenv
import os


dotenv.load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

inline_menu = telebot.types.InlineKeyboardMarkup()
btn_1 = telebot.types.InlineKeyboardButton('1')
btn_2 = telebot.types.InlineKeyboardButton('2')
btn_3 = telebot.types.InlineKeyboardButton('3')

def funs():
    pass

@bot.message_handler(commands=['start'])
def start(massage):
     bot.send_message(massage.from_used.id, 'бот запустился')
     pass


@bot.message_handler(commands=['help'])
def help(massage):
    bot.send_massage(massage.from_used.id,  'бот запустился')

    bot.infinity_polling()