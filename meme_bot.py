import os
import dotenv
import telebot
from telebot.types import Message
import requests

dotenv.load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

# Первичная загрузка мемов (занимает много времени)
img_response = requests.get('http://api.memegen.link/templates')
images_ids = {i: (data['id'], data['blank']) for i, data in enumerate(img_response.json())}
# for img_id, data in images_ids.items():
#     response = requests.get(images_ids[img_id][1])
#     image_content = response.content
#     with open(f'meme{img_id}.png', 'wb') as file:
#         file.write(image_content)
#     print(f'{img_id} готов')
# print('Готово')


# Обработчик команды /start - вывод кнопок для удобного использования бота
# Автор: Маркина Вера Артёмовна
@bot.message_handler(commands=['start'])
def start(message: Message):
    menu = telebot.types.ReplyKeyboardMarkup(row_width=3)
    favorites_button = telebot.types.KeyboardButton('ИЗБРАНАНЫЕ')
    create_button = telebot.types.KeyboardButton('СОЗДАТЬ')
    save_button = telebot.types.KeyboardButton('СОХРАНИТЬ')
    menu.add(favorites_button, create_button, save_button)
    bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=menu)


# Команда для генерации мема:
# 1 этап - выбор изображения
@bot.message_handler(commands=['meme'])
@bot.message_handler(func=lambda message: message.text.lower() == 'создать')
def get_meme_image(message: Message, id_from=0, id_to=9):
    global images_ids
    bot.send_message(
        message.chat.id,
        f'Выберите картинку для мема (от {id_from} до {id_to}) или напиши "еще"',
        reply_markup=telebot.types.ReplyKeyboardRemove())
    media = []
    for image_id in range(id_from, id_to + 1):
        media.append(telebot.types.InputMediaPhoto(open(f'meme{image_id}.png', 'rb')))
    bot.send_media_group(message.chat.id, media)
    bot.register_next_step_handler(message, answer_handler, id_from=id_from+10, id_to=id_to+10)


# Обработчик пагинации
# Автор: Маркина Вера Артёмовна
def answer_handler(message: Message, id_from: int, id_to: int):
    print(message.text)
    if message.text == 'еще':
        global images_ids
        bot.send_message(message.chat.id, f'Выберите картинку для мема (от {id_from} до {id_to}) или напиши "еще"')
        media = []
        for image_id in range(id_from, id_to + 1):
            media.append(telebot.types.InputMediaPhoto(open(f'meme{image_id}.png', 'rb')))
        bot.send_media_group(message.chat.id, media)
        bot.register_next_step_handler(message, answer_handler, id_from=id_from+10, id_to=id_to+10)
    elif message.text.isdigit():
        get_meme_top_text(message)
    # else:
    #     bot.register_next_step_handler(message, answer_handler, id_from, id_to)


# 2 этап - выбор текста сверху
# Автор: Маркина Вера Артёмовна
def get_meme_top_text(message: Message):
    global images_ids
    image_id = int(message.text)
    if image_id not in images_ids:
        bot.send_message(message.chat.id, 'Такой картинки нет')
        bot.register_next_step_handler(message, get_meme_top_text)
        return
    bot.send_message(message.chat.id, 'Введите текст над картинкой')
    bot.register_next_step_handler(message, get_meme_bottom_text, image_id)


# 3 этап - выбор текста снизу
# Автор: Маркина Вера Артёмовна
def get_meme_bottom_text(message: Message, id: int):
    top_text = message.text
    bot.send_message(message.chat.id, 'Введите текст под картинкой')
    bot.register_next_step_handler(message, meme_generator, id, top_text)


# 4 этап - генерация мема
# Автор: Маркина Вера Артёмовна
def meme_generator(message: Message, id: int, top_text: str):
    global images_ids
    bottom_text = message.text
    bot.send_message(message.chat.id, 'Идет генерация, секундочку...')
    url = f'http://api.memegen.link/images/{images_ids[id][0]}/{top_text}/{bottom_text}.png'
    response = requests.get(url)
    image_content = response.content
    with open('meme.png', 'wb') as file:
        file.write(image_content)
    with open('meme.png', 'rb') as file:
        bot.send_photo(message.chat.id, file)
    os.remove('./meme.png')


bot.infinity_polling()
