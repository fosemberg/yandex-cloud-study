#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

import telebot
from telebot import apihelper
import requests
import json
from datetime import datetime

yaToken = 'aSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFgaSdFga='
folder_id = 'abc12Dabc12Dabc12Dab'

telegram_token = '1111111111:AAAAAaaaa1_AAAAAAAaaaaaaaaaaa111111'
# ip = '165.22.36.75'
# port = '8888'
ip = '176.9.35.158'
port = '808'

proxies = {
    'https': 'https://{}:{}'.format(ip, port)
}

apihelper.proxy = proxies

bot = telebot.TeleBot(token=telegram_token)


def getSpeech(bitData):
    header = {
        'Authorization': "Bearer {}".format(yaToken)
    }
    data = bitData
    # find what next
    link = "https://stt.api.cloud.yandex.net/speech/v1/stt:recognize?folderId={}".format(folder_id)

    file = requests.post(link, data=data, headers=header)
    response = json.loads(file.text)
    return response['result']


@bot.message_handler(commands=['start'])
def handler_start(message):
    print('пользователь с id {} что-то тебе пишет'.format(message))
    bot.send_message(message.chat.id, "Добрый вечер")


@bot.message_handler(content_types=['voice'])
def voice_processing(message):

    file_info = bot.get_file(message.voice.file_id)
    file = requests.get('https://api.telegram.org/file/bot{}/{}'.format(telegram_token, file_info.file_path),
                        proxies=proxies)

    try:
        binaryContent = file.content

        # time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # with open('audiofiles/file_{}.ogg'.format(time), 'wb+') as f:
        #     f.write(binaryContent)

        text = getSpeech(binaryContent)
        bot.send_message(message.chat.id, text)
    except Exception as err:
        bot.send_message(message.chat.id, err)


@bot.message_handler(content_types=['text'])
def handler_text(message):
    print('пользователь с id {} что-то тебе пишет'.format(message))
    bot.send_message(message.chat.id, "привет")


print('Bot start')

bot.polling(none_stop=True, interval=0)
