import requests
import telebot
import json
import time
import config
url = 'https://declarator.org/api/v1/search/person-sections/?name='




bot = telebot.TeleBot(config.tokken)


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Добро пожаловать, введите ФИО")




@bot.message_handler(content_types=['text'])
def send_message(message):
    fio = message.text
    fio = fio.replace(" ","?")
    r = requests.get(url + fio)
    with open('answer.json', 'w', encoding='utf8') as f:
        json.dump(r.json(), f, indent=2, ensure_ascii=False)
    with open('answer.json', 'r', encoding='utf-8') as f:  # открываем файл на чтение
        data = json.load(f)  # загружаем из файла данные в словарь data
        count = data['count']
        if count == 0:
            bot.send_message(message.chat.id, 'Данный гражданин не найден')
        else:
            print(count)
            position = data['results'][0]['sections'][0]['position']
            if position == '':
                position = data['results'][1]['sections'][0]['position']
                print(position)






bot.polling(none_stop=True, interval=0)