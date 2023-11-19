import os
import dotenv
import telebot


dotenv.load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=["actions"])
def start(message):
    reply_menu = telebot.types.ReplyKeyboardMarkup(row_width=1)
    clue1_button = telebot.types.KeyboardButton("ИЗБРАНАНЫЕ")
    clue2_button = telebot.types.KeyboardButton("ИСКАТЬ")
    reply_menu.add(clue1_button, clue2_button)
    bot.send_message(message.chat.id, "Выберите действие", reply_markup=reply_menu)


bot.infinity_polling()
