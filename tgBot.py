import json
import requests
import telebot

import os
TOKEN = os.environ.get("BOT_TOKEN")
API_HOST = os.environ.get("API_HOST")
print("BOT_TOKEN", TOKEN)

bot = telebot.TeleBot(TOKEN)

user_data = {}
requestBody = {}
response = {}
headers = {'Content-Type' : 'application/json'}
url = API_HOST + "/api/initialize_translation"

@bot.message_handler(commands= ['start'])
def welcome(message):
    bot.send_message(message.chat.id,
                     'Welcome to the Youtube subs bot! Please enter a YT video URL')
    user_data[message.chat.id] = {}
    bot.register_next_step_handler(message, save_url)

def save_url(message):
    # url = message.text
    # user_data[message.chat.id]['link'] = url
    # bot.send_message(message.chat.id,
    #                  'Good, now specify input language')
    # bot.register_next_step_handler(message, save_lang)
    payload = json.dumps({"link": message.text, "chat_id": message.chat.id})

    request = requests.post(url, data=payload, headers=headers)

    if request.status_code == 200:
        print("Success!", request.json())
    else:
        print(f"Failed with status code {response.status_code}: {response.text}")

    response = request.json()
    if response['translation_status'] == 'translation_processing':
        bot.send_message(message.chat.id, 'translation in progress, link will arrive soon') 

#TODO: Use when ready api
def save_lang(message):
    lang = message.text
    user_data[message.chat.id]['lang'] = lang
    bot.send_message(message.chat.id,
                     'Finally, specify language you want to get subtitles')
    bot.register_next_step_handler(message, save_reslang)

def save_reslang(message):
    reslang = message.text
    user_data[message.chat.id]['reslang'] = reslang

    payload = user_data[message.chat.id]
    payload.update({"chat_id": message.chat.id})
    payload = json.dumps(payload)

    request = requests.post(url, data=payload, headers=headers)

    if request.status_code == 200:
        print("Success!", request.json())
    else:
        print(f"Failed with status code {response.status_code}: {response.text}")

    response = request.json()
    if response['translation_status'] == 'translation_processing':
        bot.send_message(message.chat.id, 'translation in progress, link will arrive soon') 
    
if __name__ == '__main__':
    print('Бот запущен!')
    bot.polling(none_stop=True, interval=0)
