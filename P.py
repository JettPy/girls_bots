import telebot
import os
import dotenv

dotenv.load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")
bot = telebot.TeleBot(API_TOKEN)

inline_menu = telebot.types.InlineKeyboardMarkup()
button_1 = telebot.types.InlineKeyboardButton("Кнопка 1", callback_data="button_1")
button_2 = telebot.types.InlineKeyboardButton("Кнопка 2", callback_data="button_2")
button_3 = telebot.types.InlineKeyboardButton("Кнопка 3", callback_data="button_3")

inline_menu.add(button_1, button_2, button_3)

reply_menu = telebot.types.ReplyKeyboardMarkup()
button_4 = telebot.types.KeyboardButton("Кнопка 4")
button_5 = telebot.types.KeyboardButton("Кнопка 5")
button_6 = telebot.types.KeyboardButton("Кнопка 6")

reply_menu.add(button_4, button_5, button_6)

@bot.message_handler(commands=["inline"])
def inline(message):
    bot.send_message(message.chat.id, "это сообщение с inline меню", reply_markup=inline_menu)


@bot.message_handler(commands=["reply"])
def reply(message):
    bot.send_message(message.chat.id, "это сообщение с reply меню", reply_markup=reply_menu)


@bot.message_handler(commands=["clear"])
def clear(message):
    bot.send_message(message.chat.id, "это сообщение с удаляет меню", reply_markup=telebot.types.ReplyKeyboardRemove())


@bot.callback_query_handlers(func = lambda call: call.date)
def query_handler(call):
    if call.date == "button_1":
        bot.send_message(call.messege.chat.id, "вы нажали кнопку 1")
    elif call.date == "button_2":
        bot.send_message(call.messege.chat.id, "вы нажали кнопку 2")
    elif call.date == "button_3":
        bot.send_message(call.messege.chat.id, "вы нажали кнопку 3")

bot.infinity_polling()
