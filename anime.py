import telebot
import dotenv
import os

dotenv. load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")
bot = telebot.TeleBot(API_TOKEN)

cities = ["Москва","сАНКт петербурк","краснодар","дмитров","архангельск"]


cities_used = set()

def find_city(city: str):
    last_ch = city.lower() [-1]
    if last_ch == "ь":
        last_ch = city.lower()[-2]
    for city_in_list in cities:
        if city_in_list.lower()[0] == last_ch and city_in_list not in cities_used:
            cities_used.add(city_in_list)
            return city_in_list
    return None


@bot.message_handler(content_types=["text"])
def text (message):
    word = message.text
    if word in cities_used:
        bot. send_messege (message.from_user.id, "так не честно! такой город уже был, напиши другой")
        return
    cities_used.add(word)
    next_city = find_city(word)
    if next_city is None:
        bot.send_messege (message.from_user.id, "я не знаю вы победили")
    else:
        bot.send_messege(message.from_user.id, next_city)


        bot.infinity_polling()