import datetime
import time
import json
import os
import requests
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton

from config import TOKEN, PROXY
from utils import course_to_str, course_to_str, get_user

def handle(msg):
    
    content_type, chat_type, chat_id = telepot.glance(msg)
    if chat_type == u'private' and content_type == 'text':
        # print(get_user(chat_id).search_course(msg['text']))
        # print([course_to_str(c) for c in get_user(chat_id).search_course(msg['text'])])
        bot.sendMessage(chat_id,
        '\n\n'.join([course_to_str(c) for c in get_user(chat_id).search_course(msg['text'])])
        )



if PROXY:
    telepot.api.set_proxy(PROXY)

bot = telepot.Bot(TOKEN)
MessageLoop(bot, handle).run_as_thread()

while True:
    time.sleep(30)