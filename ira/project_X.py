import telebot
import os
import dotenv
import re
import urllib
import requests

dotenv.load_dotenv()
API_TOKEN = os.detenv("API_TOKEN")

url = "http://www.youtube.com/resulte?"

regexp = "(?<=/watch\?v=)[\w-]{11}"

pattern = re.compile(regexp)