import time
# import datetime
# import json
# import os
# import requests

import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton

from config import TOKEN, PROXY
from utils import save_users, course_to_str, course_to_str, get_user, MenuState, search_department, all_departments


def keyboard_maker(keyboard_labels):
    my_keyboard = []
    for row in keyboard_labels:
        keyboard_row = []
        for label in row:
            keyboard_row.append(KeyboardButton(text=label))

        my_keyboard.append(keyboard_row)

    return ReplyKeyboardMarkup(keyboard=my_keyboard, resize_keyboard=True)


def send_welcome_message(chat_id):
    bot.sendMessage(chat_id,
                    'لطفا از منوی بات گزینه مورد نظرتان را انتخاب کنید',
                    'Markdown',
                    reply_markup=keyboard_maker([
                        ['انتخاب بخش'],
                        ['جستجوی درس های بخش'],
                        ['درس های انتخاب شده']
                    ]))


def send_select_department_message(chat_id):
    bot.sendMessage(chat_id,
                    '''بخش كامپيوتر /dep2903
بخش مهندسي قدرت و كنترل /dep2901
بخش مهندسي مخابرات و الكترونيك /dep2902
بخش مواد /dep1002
بخش رياضي /dep1103
بخش امار /dep1104
بخش فيزيك /dep1106
بخش زبـان وادبيات فارسي /dep1205
بخش زبـانهاي خارجي وزبان شناسي /dep1206
بخش فلسفه و كلام اسلامي /dep3401
بخش علوم قرآن و فقه /dep3402
بخش عمومي /dep2701
بخش برق /dep2703'''
                    )
    bot.sendMessage(chat_id,
                    'لطفا بخش مورد نظر را انتخاب یا تمام یا قسمتی از نام بخش مورد نظر را وارد کنید',
                    'Markdown',
                    reply_markup=keyboard_maker([
                        ['بازگشت']
                    ]))


def send_search_course_message(chat_id):
    bot.sendMessage(chat_id,
                    'لطفا تمام یا قسمتی از نام درس مورد نظر را وارد کنید',
                    'Markdown',
                    reply_markup=keyboard_maker([
                        ['بازگشت']
                    ]))


def send_not_found_message(chat_id):
    bot.sendMessage(chat_id,
                    'موردی یافت نشد',
                    'Markdown',
                    reply_markup=keyboard_maker([
                        ['بازگشت']
                    ]))


def bot_messages_generator(message_pieces):
    messages = []
    message = ''

    msg_max_length = 4096
    for piece in message_pieces:
        if len(message + piece) >= msg_max_length:
            messages.append(message)
            message = ''
        message += piece
    if len(message) > 0:
        messages.append(message)
    return messages


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if chat_type == u'private' and content_type == 'text':
        user = get_user(chat_id)
        # print(get_user(chat_id).search_course(msg['text']))
        # print([course_to_str(c) for c in get_user(chat_id).search_course(msg['text'])])
        if msg['text'][0:4] == '/del':
            user.remove_course(msg['text'][4:])
            courses = user.get_courses()
            if len(courses) == 0:
                send_not_found_message(chat_id)
            else:
                messages = bot_messages_generator([course_to_str(c) + '\n/del' + c['ident'] + '\n\n' for c in courses])
                for message in messages:
                    bot.sendMessage(chat_id,
                                    message
                                    )
            send_welcome_message(chat_id)
        elif msg['text'][0:4] == '/add':
            user.add_course(msg['text'][4:])
            bot.sendMessage(chat_id,
                            'با موفقیت ثبت شد'
                            )
            send_search_course_message(chat_id)
        elif user.menu_state == MenuState.GENERAL:
            if msg['text'] == 'انتخاب بخش':
                user.menu_state = MenuState.SELECT_DEPARTMENT
                send_select_department_message(chat_id)
            elif msg['text'] == 'جستجوی درس های بخش':
                user.menu_state = MenuState.SEARCH_COURSE
                send_search_course_message(chat_id)
            elif msg['text'] == 'درس های انتخاب شده':
                courses = user.get_courses()
                if len(courses) == 0:
                    send_not_found_message(chat_id)
                else:
                    messages = bot_messages_generator(
                        [course_to_str(c) + '\n/del' + c['ident'] + '\n\n' for c in courses])
                    for message in messages:
                        bot.sendMessage(chat_id,
                                        message
                                        )
            else:
                send_welcome_message(chat_id)

        elif user.menu_state == MenuState.SELECT_DEPARTMENT:

            if msg['text'] == 'بازگشت':
                user.menu_state = MenuState.GENERAL
                send_welcome_message(chat_id)

            elif msg['text'][0:4] == '/dep':
                user.dep_id = msg['text'][4:]
                bot.sendMessage(chat_id,
                                'با موفقیت ثبت شد'
                                )
                user.menu_state = MenuState.SEARCH_COURSE
                send_search_course_message(chat_id)

            else:
                departments = search_department(msg['text'])
                if len(departments) == 0:
                    send_not_found_message(chat_id)
                else:
                    messages = bot_messages_generator(
                        [dep['title'] + ' ' + '/dep' + dep['id'] + '\n' for dep in departments])
                    for message in messages:
                        bot.sendMessage(chat_id,
                                        message
                                        )

        elif user.menu_state == MenuState.SEARCH_COURSE:

            if msg['text'] == 'بازگشت':
                user.menu_state = MenuState.GENERAL
                send_welcome_message(chat_id)

            else:
                courses = user.search_course(msg['text'])
                if len(courses) == 0:
                    send_not_found_message(chat_id)
                else:
                    messages = bot_messages_generator(
                        [course_to_str(c) + '\n/add' + c['ident'] + '\n\n' for c in courses])
                    for message in messages:
                        bot.sendMessage(chat_id,
                                        message
                                        )


if __name__ == '__main__':
    if PROXY:
        telepot.api.set_proxy(PROXY)

    bot = telepot.Bot(TOKEN)
    MessageLoop(bot, handle).run_as_thread()

    save_time_delay = 2 * 60 * 60
    while True:
        time.sleep(save_time_delay)
        save_users()
