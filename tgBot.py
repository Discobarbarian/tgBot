import json
import requests
import telebot
from telebot import types
from config import TOKEN
from copy import deepcopy

bot = telebot.TeleBot(TOKEN)

user_data = {}
requestBody = {}
response = {}
header = {'Content-Type' : 'application/json'}

@bot.message_handler(commands= ['start'])
def welcome(message):
    bot.send_message(message.chat.id,
                     'Welcome to the Youtube subs bot! Please enter a YT video URL')
    user_data[message.chat.id] = {}
    bot.register_next_step_handler(message, save_url)

def save_url(message):
    url = message.text
    user_data[message.chat.id]['link'] = url
    bot.send_message(message.chat.id,
                     'Good, now specify input language')
    bot.register_next_step_handler(message, save_lang)

def save_lang(message):
    lang = message.text
    user_data[message.chat.id]['lang'] = lang
    bot.send_message(message.chat.id,
                     'Finally, specify language you want to get subtitles')
    bot.register_next_step_handler(message, save_reslang)

def save_reslang(message):
    reslang = message.text
    user_data[message.chat.id]['reslang'] = reslang
    #print(user_data)
    #print(user_data[message.chat.id])
    requestBody = deepcopy(user_data[message.chat.id])
    requestBody['chat_id'] = message.chat.id
    payload = json.dumps(requestBody)
    print(payload)

    request = requests.post('http://85.209.9.165:8080/api/initialize_translation', headers= header, json= payload)
    print(request)
    print(request.text)
    print(user_data)
    print(request.headers)

    response = json.loads(request.text)
    if response['translation_status'] == 'translation_processing':
        bot.send_message(message.chat.id, 'translation in progress, link will arrive soon') 
    
    



if __name__ == '__main__':
    print('Бот запущен!')
    bot.polling(none_stop=True, interval=0)