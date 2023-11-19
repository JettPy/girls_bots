import os
import dotenv
import telebot
from telebot.types import Message

dotenv.load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")
bot = telebot.TeleBot(API_TOKEN)


# Обработчик команды /actions - вывод кнопок для удобного использования бота
# Автор: Маркина Вера Артёмовна
@bot.message_handler(commands=["actions"])
def start(message: Message):
    inline_menu = telebot.types.InlineKeyboardMarkup(row_width=1)
    favorites_button = telebot.types.InlineKeyboardButton("ИЗБРАНАНЫЕ", callback_data="favorites")
    search_button = telebot.types.InlineKeyboardButton("ИСКАТЬ", callback_data="search")
    # TODO Возможно тут добавим еще одну кнопку
    inline_menu.add(favorites_button, search_button)
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=inline_menu)


# Обработчик нажатых кнопок меню
# Автор: Маркина Вера Артёмовна
@bot.callback_query_handler(func=lambda call: call.data)
def button_handlers(call):
    # TODO Доделать обработку нажатия кнопок
    pass


bot.infinity_polling()
