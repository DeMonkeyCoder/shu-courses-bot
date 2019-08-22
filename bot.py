import datetime
import time
import json
import os
import requests
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton

from config import TOKEN, PROXY


def handle(msg):
    
    content_type, chat_type, chat_id = telepot.glance(msg)
    if chat_type == u'private' and content_type == 'text':
        bot.sendMessage(chat_id,
                    'hi')



if PROXY:
    telepot.api.set_proxy(PROXY)

bot = telepot.Bot(TOKEN)
MessageLoop(bot, handle).run_as_thread()

while True:
    time.sleep(30)