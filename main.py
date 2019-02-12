import requests
import telebot
import json
import time
url = 'https://declarator.org/api/v1/search/person-sections/?name='




bot = telebot.TeleBot('586569609:AAGkb_-IPu3qy9kZX9En2hJGHp-TUaCqqsI')


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Добро пожаловать, введите ФИО")




@bot.message_handler(content_types=['text'])
def send_message(message):
    fio = message.text
    fio = fio.replace(" ","?")
    chat_id = message.chat.id
    get_updates(fio)



def get_updates(fio):
    r = requests.get(url + fio)
    print(r.encoding)


    write_json(r.json())




def convert():
    with open('answer.json', 'r', encoding='utf-8') as fh:  # открываем файл на чтение
        data = json.load(fh)  # загружаем из файла данные в словарь data
        count = data['count']
        if count == 0:
            pass

        position = data['results'][0]['sections'][0]['position']
        print(position)
        if position == '':
            position = data['results'][1]['sections'][0]['position']
            print(position)
    


def write_json(data, filename='answer.json'):
    with open(filename, 'w', encoding='utf8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    convert()




bot.polling(none_stop=True, interval=0)