import requests
import os
import datetime

import telebot
from telebot.types import Message, Sticker
from telebot import apihelper, types

PROXY = 'https://user:password@54.36.109.28:3128'

TOKEN = '756220589:AAHPb01VMQOoBsgwJbe6iSlD9nuhVgIWEKA'

apihelper.proxy = {'https': PROXY}
proxies = apihelper.proxy
bot = telebot.TeleBot(TOKEN)


def scan(filename, mode='color', res='300'):

    os.system('hp-scan --mode={} --res={} --file={}'.format(mode,res,filename))

    if os.path.exists(filename):
        return True
    else:
        return False


@bot.message_handler(commands=['start'])
def send_welcome(message: Message):
    chat_id = message.chat.id
    user_dict = message.from_user
    user_id = user_dict.id
    bot.send_message(chat_id, 'Добро пожаловать, {}'.format(user_dict.first_name))
    user=open('{}'.format(user_id), 'w')
    user.writelines('{},{},{}'.format(user_dict.username,user_dict.first_name,user_dict.last_name))
    user.close()

    # markup = types.InlineKeyboardMarkup(row_width=2)
    # btn_print = types.InlineKeyboardButton('Printing',)
    # btn_scan = types.InlineKeyboardButton('Scanning')
    # markup.add(btn_print, btn_scan)
    # bot.send_message(chat_id, "Choose mode", reply_markup=markup)

@bot.message_handler(commands=['scan'])
def scan_image(message: Message):
    chat_id = message.chat.id
    user_dict = message.from_user
    user_id = user_dict.id
    #    filename = f'{datetime.datetime.year}{datetime.datetime.month}{datetime.datetime.day}{datetime.datetime.hour}{datetime.datetime.minute}{datetime.datetime.second}.jpg'

    if os.path.exists('{}'.format(user_id)):
        filename = 'test.jpg'
        bot.send_message(chat_id, 'Дождитесь окончания сканиования...')
        if scan(filename):
            bot.send_message(chat_id, 'Сканирование завершено успешно!')
        else:
            bot.send_message(chat_id, 'Сканирование не удалось!')
        with open(filename, 'rb') as image:
            bot.send_photo(chat_id,image)
        os.remove(filename)

    else:
        bot.send_message(chat_id,'Необходимо запустить бота командой /start!')


bot.polling()
