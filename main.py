import requests
import telebot
from telebot import types
import os

token = os.environ.get('API_TOKEN')
wisperUrl = os.environ.get('WISPER_URL')
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bot.send_message(message.from_user.id, "👋", reply_markup=markup)

@bot.message_handler(content_types=['text', 'audio', 'voice'])
def get_text_messages(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if message.voice:
        bot.send_message(message.from_user.id, "Waiting...", reply_markup=markup)
        file_info = bot.get_file(message.voice.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        files = {'audio_file': ('sample.ogg', downloaded_file, 'audio/ogg')}
        url = f'{wisperUrl}/asr?task=transcribe&encode=true&output=txt&word_timestamps=false'
        headers = {
            "accept": "application/json"
        }
        response = requests.post(url, headers=headers, files=files)
        bot.send_message(message.from_user.id, response.content, reply_markup=markup)
    else:
        bot.send_message(message.from_user.id, 'Non audio message', reply_markup=markup)


bot.polling(none_stop=True, interval=0)