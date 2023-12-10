import json
import sqlite3
import telebot
from telebot.types import Message
import os
import dotenv
import requests

dotenv.load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')
bot = (telebot.TeleBot(API_TOKEN))

# Подключение к базе данных
# Автор: Маркина Ирина Артёмовна
connection = sqlite3.connect('memebot.sqlite', check_same_thread=False)  # Подключение базе данных
cursor = connection.cursor()

# Создание таблицы для хранения записей пользователей
cursor.execute('''CREATE TABLE IF NOT EXISTS memes(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL, 
                    meme BLOB NOT NULL
                )''')
connection.commit()  # Подключение к базе данных


# Обработчик командны сохранения мема
# Автор: Маркина Ирина Артёмовна
@bot.message_handler(commands=['save'])
def save_handler(message: Message):
    bot.send_message(message.chat.id, "Хорошо, пришлите мне мем, я его сохраню")
    bot.register_next_step_handler(message, save_to_database)


# Сохранение мема в базе данных
# Автор: Маркина Ирина Артёмовна
def save_to_database(message: Message):
    if message.photo:
        user = message.from_user.username
        meme_info = bot.get_file(message.photo[-1].file_id)
        meme = bot.download_file(meme_info.file_path)
        cursor.execute('''INSERT INTO memes (username, meme) VALUES (?, ?)''', (user, meme))
        connection.commit()
        bot.send_message(message.chat.id, 'Мем сохранен в избранное')
    else:
        bot.send_message(message.chat.id, 'Это не картинка... Попробуй еще раз')


# Получение сохраненных мемов
# Автор: Маркина Ирина Артёмовна
@bot.message_handler(commands=['favourite'])
def favourite_handler(message: Message):
    bot.send_message(message.chat.id, "Вот ваши мемы:")
    cursor.execute('''SELECT meme FROM memes WHERE username = ?''', (message.from_user.username,))
    memes = cursor.fetchall()
    # Отправляем пользователю все сохраненные мемы
    for meme in memes:
        bot.send_photo(message.chat.id, meme[0])


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
