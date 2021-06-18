import subprocess
import os

import telebot
import pdftotext

from core.models import User, Files

import requests
import tempfile

import traceback

import sys

from pdf_bot.settings import TELEGRAM_TOKEN, DEBUG

bot = telebot.TeleBot(TELEGRAM_TOKEN)

if DEBUG:
    url = 'https://a4ef15322027.ngrok.io/telegram_bot_path' # запуск ngrok(директория home) ./ngrok http 8000 , сайт https://ngrok.com/
else:
    url = 'https://from-pdf-bot.herokuapp.com/telegram_bot_path'

bot.set_webhook(url=url)

@bot.message_handler(commands=['start'])
def hand_start_messate(message):
    resp = '/start - информация о боте\nБот конвертирует файлы PDF в формат txt\nОтправъте файл PDF в сообщении для конвертации в формат txt'
    bot.send_message(chat_id=message.chat.id, text=resp)
    call_user(message)


@bot.message_handler(commands=['output_format'])
def hand_output_format(message):
    resp = 'Формат задан'
    bot.send_message(chat_id=message.chat.id, text=resp)

@bot.message_handler(content_types=['document'])
def hand_pdf_to_txt(message):
    file_to_convert = get_file_to_convert(message)
    user = call_user(message)
    save_file(user, message)
    if message.document.mime_type == 'application/pdf':
        pdf = text_pdf_from_txt(file_to_convert)
        send_pdf_file(message, pdf)
    elif message.document.mime_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        convert_to_pdf(message, file_to_convert)
    else:
        resp = 'Не могу конвертировать из этого формата'
        bot.send_message(chat_id=message.chat.id, text=resp)
    #user = User.objects.filter(chat_id=message.chat.id)
    #user = user.get() if user else User.objects.create(chat_id=message.chat.id)
    #user.save()

def send_pdf_file(message, pdf):
    with tempfile.NamedTemporaryFile(mode='a+', suffix='.txt') as temp_pdf_file:
        for page in pdf:
            temp_pdf_file.write(page)
        temp_pdf_file.seek(0)
        bot.send_document(chat_id=message.chat.id, data=temp_pdf_file)

def text_pdf_from_txt(file_to_convert):
    with tempfile.NamedTemporaryFile(suffix='.txt') as temp_file_to_convert:
        temp_file_to_convert.write(file_to_convert)
        temp_file_to_convert.seek(0)
        return pdftotext.PDF(temp_file_to_convert)

def get_file_to_convert(message):
    file_id = message.document.file_id
    file_info = bot.get_file(file_id)
    return requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(TELEGRAM_TOKEN, file_info.file_path)).content

def process_telegram_event(update_json):
    update = telebot.types.Update.de_json(update_json)
    bot.process_new_updates([update])

def call_user(message):
    user = User.objects.filter(chat_id=message.chat.id)
    user = user.get() if user else User.objects.create(chat_id=message.chat.id, username=message.from_user.username, is_bot=message.from_user.is_bot)
    return user

def save_file(user, message):
    try:
        Files.objects.create(
            user=user, file_id=message.document.file_id, file_unique_id=message.document.file_unique_id,
            mime_type=message.document.mime_type, file_size=message.document.file_size
        )
    except Exception as err:
        message_error = err.args[0]
        bot.send_message(chat_id=246241639, text=message_error.strip())

def convert_to_pdf(message, docx_to_convert):
    cur_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    with tempfile.NamedTemporaryFile(suffix='.docx', dir=cur_dir) as temp_file_to_convert:
        try:
            temp_file_to_convert.write(docx_to_convert)
            temp_file_to_convert.seek(0)
            name_file = temp_file_to_convert.name
            args = ['libreoffice', '--headless', '--convert-to', 'pdf', name_file]
            subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            result_file = name_file.split('.')[0] + '.pdf'
            with open(f'{result_file}', 'br') as f:
                bot.send_document(chat_id=message.chat.id, data=f)
            os.remove(result_file)
        except Exception:
            traceback.print_exc(file=sys.stdout)
