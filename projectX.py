import telebot
import os
import dotenv
import re
import urllib
import requests


dotenv.load_dotenv()
API_TOKEN = os.getenv('API_TOKEN')
bot = (telebot.TeleBot(API_TOKEN))

url = 'http://www.youtube.com/results?'

regext = '(?<=/watch\?v=)[|w-]{11}'

pattern = re. compile(regexp)

@bot.message_handler(content_types=['text'])
def get_text_message(message):   