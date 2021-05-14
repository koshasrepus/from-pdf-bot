import telebot
import requests
import math

from pdf_bot.settings import TELEGRAM_TOKEN, DEBUG

bot = telebot.TeleBot(TELEGRAM_TOKEN)

if DEBUG:
    url = 'https://5a3b121a18fd.ngrok.io/telegram_bot_path' # запуск ngrok(директория home) ./ngrok http 8000 , сайт https://ngrok.com/
else:
    url = 'https://app-my-places.herokuapp.com/telegram_bot_path'

bot.set_webhook(url=url)

@bot.message_handler(commands=['start'])
def hand_start_messate(message):
    resp = '/start - информация о боте\n/add - добавить локацию\n/list - просмотр 10 последних локаций\n' \
           '/reset - удалить все локации\nМожно отправить локацию, чтобы просмотреть сохранённые места в радиусе 500 метров'
    bot.send_message(chat_id=message.chat.id, text=resp)


def process_telegram_event(update_json):
    update = telebot.types.Update.de_json(update_json)
    bot.process_new_updates([update])

#bot = telebot.TeleBot(TELEGRAM_TOKEN)

#bot.set_webhook(url='http://faf5f0bff88a.ngrok.io')