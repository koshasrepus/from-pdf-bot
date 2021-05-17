import telebot
import pdftotext

import requests
import tempfile


from pdf_bot.settings import TELEGRAM_TOKEN, DEBUG

bot = telebot.TeleBot(TELEGRAM_TOKEN)

if DEBUG:
    url = 'https://b16fcd18fac3.ngrok.io/telegram_bot_path' # запуск ngrok(директория home) ./ngrok http 8000 , сайт https://ngrok.com/
else:
    url = 'https://from-pdf-bot.herokuapp.com/telegram_bot_path'

bot.set_webhook(url=url)

@bot.message_handler(commands=['start'])
def hand_start_messate(message):
    resp = '/start - информация о боте\nБот конвертирует файлы PDF в формат txt\nОтправъте файл PDF в сообщении для конвертации в формат txt'
    bot.send_message(chat_id=message.chat.id, text=resp)

@bot.message_handler(commands=['output_format'])
def hand_output_format(message):
    resp = 'Формат задан'
    bot.send_message(chat_id=message.chat.id, text=resp)

@bot.message_handler(content_types=['document'])
def hand_pdf_to_txt(message):
    file_to_convert = get_file_to_convert(message)
    pdf = text_pdf_from_txt(file_to_convert)
    send_pdf_file(message, pdf)

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

