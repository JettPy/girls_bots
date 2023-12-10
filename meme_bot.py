import os
import dotenv
import telebot
from telebot.types import Message
import requests

dotenv.load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")
bot = telebot.TeleBot(API_TOKEN)


user = ''

# Обработчик команды /actions - вывод кнопок для удобного использования бота
# Автор: Маркина Вера Артёмовна
@bot.message_handler(commands=["start"])
def start(message: Message):
    inline_menu = telebot.types.InlineKeyboardMarkup(row_width=1)
    favorites_button = telebot.types.InlineKeyboardButton("ИЗБРАНАНЫЕ", callback_data="favorites")
    create_button = telebot.types.InlineKeyboardButton("СОЗДАТЬ", callback_data="create")
    inline_menu.add(favorites_button, create_button)
    global user
    user = message.chat.id
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=inline_menu)


# Обработчик нажатых кнопок меню
# Автор: Маркина Вера Артёмовна
@bot.callback_query_handler(func=lambda call: call.data)
def button_handlers(call):
    global user
    if call.data == "favorites":
        favorites(call.data.message)
    elif call.data == "create":
        # bot.send_message(user, call)
        create_from_user(call.from_user.id)


def favorites(message: Message):
    pass


def create(message: Message):
    global images_ids
    img_response = requests.get("http://api.memegen.link/templates")
    images_data = img_response.json()
    images_ids = {data["id"] for data in images_data}
    bot.send_message(message.from_user.id, ", ".join(images_ids))
    bot.send_message(message.from_user.id, "Выберите картинку для мема")
    bot.register_next_step_handler(message, get_meme_top_text)


def create_from_user(user_id):
    global images_ids
    img_response = requests.get("http://api.memegen.link/templates")
    images_data = img_response.json()
    images_ids = {data["id"] for data in images_data}
    bot.send_message(user_id, ", ".join(images_ids))
    bot.send_message(user_id, "Выберите картинку для мема")
    bot.register_next_step_handler(user_id, get_meme_top_text)



# Временная константа:
images_ids = set()


# Команда для генерации мема:
# 1 этап - выбор изображения
@bot.message_handler(commands=["meme"])
def get_meme_image(message: Message):
    favorites(message)


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
