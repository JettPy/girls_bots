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
conn = sqlite3.connect("memebot.db", check_same_thread=False) # Подключение базе данных
cursor = conn.cursor()

# Создание таблицы для хранения записей пользователей
cursor.execute('''CREATE TABLE IF NOT EXISTS users
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   username TEXT,
                   password TEXT)''')
conn.commit() # Подключение к базе данных

# Создание таблицы для хранения записей мемов
cursor.execute('''CREATE TABLE IF NOT EXISTS memes
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   meme BLOB)''')
conn.commit()

# Создание таблицы для хранения записей любимых мемов
cursor.execute('''CREATE TABLE IF NOT EXISTS favorites
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   user_id INTEGER,
                   meme_id INTEGER)''')
conn.commit()


# Регистрация пользователя в базе данных
# Автор: Маркина Ирина Артёмовна
@bot.message_handler(commands=['start'])
def text(message: Message):
    # TODO Реализовать работу по регистрации пользователя в базе данных
    pass
    # bot.register_next_step_handler()


bot.infinity_polling()
