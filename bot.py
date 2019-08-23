import datetime
import time
import json
import os
import requests
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton

from config import TOKEN, PROXY
from utils import course_to_str, course_to_str, get_user, MenuState, search_department

def send_welcome_message(chat_id):
    bot.sendMessage(chat_id,
        'لطفا از منوی بات گزینه مورد نظرتان را انتخاب کنید',
        'Markdown',
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="انتخاب بخش")
                ],
                [
                    KeyboardButton(text="جستجوی درس های بخش")
                ],
                [
                    KeyboardButton(text="درس های انتخاب شده")
                ],
            ]
        ),
    )

def send_select_department_message(chat_id):
    bot.sendMessage(chat_id,
        'لطفا تمام یا قسمتی از نام بخش مورد نظر را وارد کنید',
        'Markdown',
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="بازگشت")
                ],
            ]
        ),
    )

def send_search_course_message(chat_id):
    bot.sendMessage(chat_id,
        'لطفا تمام یا قسمتی از نام درس مورد نظر را وارد کنید',
        'Markdown',
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="بازگشت")
                ],
            ]
        ),
    )

def send_not_found_message(chat_id):
    bot.sendMessage(chat_id,
        'موردی یافت نشد',
        'Markdown',
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="بازگشت")
                ],
            ]
        ),
    )

def handle(msg):
    
    content_type, chat_type, chat_id = telepot.glance(msg)
    if chat_type == u'private' and content_type == 'text':
        user = get_user(chat_id)
        # print(get_user(chat_id).search_course(msg['text']))
        # print([course_to_str(c) for c in get_user(chat_id).search_course(msg['text'])])
        if(user.menu_state == MenuState.GENERAL):
            if(msg['text'] == 'انتخاب بخش'):
                user.menu_state = MenuState.SELECT_DEPARTMENT
                send_select_department_message(chat_id)
            elif(msg['text'] == 'جستجوی درس های بخش'):
                user.menu_state = MenuState.SEARCH_COURSE
                send_search_course_message(chat_id)
            else:
                send_welcome_message(chat_id)

        elif(user.menu_state == MenuState.SELECT_DEPARTMENT):

            if(msg['text'] == 'بازگشت'):
                user.menu_state = MenuState.GENERAL
                send_welcome_message(chat_id)

            elif(msg['text'][0:4] == '/dep'):
                user.dep_id = msg['text'][4:]
                bot.sendMessage(chat_id,
                    'با موفقیت ثبت شد'
                )
                user.menu_state = MenuState.GENERAL
                send_welcome_message(chat_id)

            else:
                departments = search_department(msg['text'])
                if len(departments) == 0:
                    send_not_found_message(chat_id)
                else:
                    bot.sendMessage(chat_id,
                        '\n\n'.join([dep['title'] + '\n' + '/dep' + dep['id'] for dep in departments])
                    )
                    
        elif(user.menu_state == MenuState.SEARCH_COURSE):
        
            if(msg['text'] == 'بازگشت'):
                user.menu_state = MenuState.GENERAL
                send_welcome_message(chat_id)

            else:
                courses = user.search_course(msg['text'])
                if len(courses) == 0:
                    send_not_found_message(chat_id)
                else:
                    bot.sendMessage(chat_id,
                        '\n\n'.join([course_to_str(c) for c in courses])
                    )


if PROXY:
    telepot.api.set_proxy(PROXY)

bot = telepot.Bot(TOKEN)
MessageLoop(bot, handle).run_as_thread()

while True:
    time.sleep(30)