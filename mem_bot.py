import sqlite3
import telebot
import os
import dotenv


dotenv.load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')
bot = (telebot.TeleBot(API_TOKEN))


# Подключение базе данных
conn = sqlite3.connect('memebot.db', check_same_thread=False)
cursor = conn.cursor()

# Создание таблицы для хранения записей

cursor.execute('''CREATE TABLE IF NOT EXISTS users
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   username TEXT,
                   password TEXT)''')
conn.commit() # Подключение к базе данных

cursor.execute('''CREATE TABLE IF NOT EXISTS memes
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   meme TEXT)''')
conn.commit() # Подключение к базе данных

cursor.execute('''CREATE TABLE IF NOT EXISTS favorites
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   user_id INTEGER,
                   meme_id INTEGER)''')
conn.commit() # Подключение к базе данных




bot.infinity_polling()