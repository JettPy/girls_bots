import sqlite3
import telebot
from telebot.types import Message
import os
import dotenv
import requests

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


# Временная константа:
images_ids = set()


# Команда для генерации мема:
# 1 этап - выбор изображения
@bot.message_handler(commands=["meme"])
def get_meme_image(message: Message):
    global images_ids
    img_response = requests.get("http://api.memegen.link/templates")
    images_data = img_response.json()
    images_ids = {data["id"] for data in images_data}
    bot.send_message(message.from_user.id, ", ".join(images_ids))
    bot.send_message(message.from_user.id, "Выберите картинку для мема")
    bot.register_next_step_handler(message, get_meme_top_text)


# 2 этап - выбор текста сверху
def get_meme_top_text(message: Message):
    global images_ids
    image_id = message.text
    if image_id not in images_ids:
        bot.send_message(message.from_user.id, "Такой картинки нет, конец операции")
        return
    bot.send_message(message.from_user.id, "Введите текст над картинкой")
    bot.register_next_step_handler(message, get_meme_bottom_text, image_id)


# 3 этап - выбор текста снизу
def get_meme_bottom_text(message: Message, id: str):
    top_text = message.text
    bot.send_message(message.from_user.id, "Введите текст под картинкой")
    bot.register_next_step_handler(message, meme_generator, id, top_text)


# 4 этап - генерация мема
def meme_generator(message: Message, id: str, top_text: str):
    bottom_text = message.text
    bot.send_message(message.from_user.id, "Идет генерация, секундочку...")
    url = f"http://api.memegen.link/images/{id}/{top_text}/{bottom_text}.png"
    response = requests.get(url)
    image_content = response.content
    with open("meme.png", "wb") as file:
        file.write(image_content)
    with open("meme.png", "rb") as file:
        bot.send_photo(message.from_user.id, file)
    os.remove("./meme.png")


bot.infinity_polling()
