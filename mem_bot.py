import sqlite3
import telebot
from telebot.types import Message
import os
import dotenv

dotenv.load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")
bot = (telebot.TeleBot(API_TOKEN))

# Подключение к базе данных
# Автор: Маркина Ирина Артёмовна
conn = sqlite3.connect("memebot.db", check_same_thread=False)  # Подключение базе данных
cursor = conn.cursor()


# Создание таблицы для хранения записей мемов
cursor.execute('''CREATE TABLE IF NOT EXISTS memes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                meme BLOB
                )''')
conn.commit()


# Регистрация пользователя в базе данных
# Автор: Маркина Ирина Артёмовна
@bot.message_handler(commands=['save'])
def save(message: Message):
    bot.send_message(message.from_user.id, 'пришлите мем!!!')
    bot.register_next_step_handler(message, upload_meme)


def upload_meme(message: Message):
    with open("meme.jpg","rd") as file:
        image_blob = file.read()
    cursor.execute('''
    INSERT INTO memes(username, meme)
    VALUES(??)
    ''', (message.from_user.username, image_blob))
    conn.commit()
    # bot.register_next_step_handler()


@bot.message_handler(commands=['favorite'])
def favorite(message: Message):
    pass


bot.infinity_polling()
