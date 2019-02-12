import requests
import telebot
import json
import time
import config
url = 'https://declarator.org/api/v1/search/person-sections/?name='




bot = telebot.TeleBot(config.tokken)


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Добро пожаловать, данный БОТ позволяет осуществлять поиск в открытых источниках деклорации чиновников")




@bot.message_handler(content_types=['text'])
def send_message(message):
    fio = message.text
    fio = fio.replace(" ","?")
    bot.send_message(message.chat.id, 'Секундочку ищу его')
    time.sleep(0.30)
    r = requests.get(url + fio)
    with open('answer.json', 'w', encoding='utf8') as f:
        json.dump(r.json(), f, indent=2, ensure_ascii=False)
    with open('answer.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        count = data['count']
        if count == 0:
            bot.send_message(message.chat.id, 'Данный гражданин не найден')
        elif count > 2:
            bot.send_message(message.chat.id, 'Найдено ' + str(count) + ' гражданин, пожалуйста попробуйте уточнить ФИО')
        else:
            print(count)
            position = data['results'][0]['sections'][0]['position']
            if position == '':
                position = data['results'][1]['sections'][0]['position']

                yaer = data['results'][1]['sections'][0]['sections'][0]['main']['year']
                income = data['results'][1]['sections'][0]['sections'][0]['incomes'][0]['size']



                bot.send_message(message.chat.id, 'Данные за '+ str(yaer)+ ' год, должность: ' + str(position)+ ', доход составил: ' +str(income)+ ' ₽')
                try:
                    wife = data['results'][1]['sections'][0]['sections'][0]['incomes'][1]['size']
                    bot.send_message(message.chat.id, 'Доход супруги: ' + str(wife)+ ' ₽')
                except Exception as ex:
                    print('Нет супргуги')


            else:
                yaer = data['results'][0]['sections'][0]['sections'][0]['main']['year']
                income = data['results'][0]['sections'][0]['sections'][0]['incomes'][0]['size']


                bot.send_message(message.chat.id, 'Данные за ' + str(yaer) + ' год, должность: ' + str(
                    position) + ', доход составил: ' + str(income) + ' ₽')
                try:
                    wife = data['results'][0]['sections'][0]['sections'][0]['incomes'][1]['size']
                    bot.send_message(message.chat.id, 'Доход супруги: ' + str(wife)+ ' ₽')
                except Exception as ex:
                    print('Нет супргуги')







bot.polling(none_stop=True, interval=0)