import requests
import telebot
import os
from flask import Flask, request
from lxml import html
from threading import Thread
from time import sleep


TOKEN = ""

bot = telebot.TeleBot(TOKEN)

server = Flask(__name__)

global chat_id


def telegram_bot_sendtext(bot_message):
    global chat_id
    bot.send_message(chat_id, bot_message)


def show_weather(city):
    key = ""
    get_weather = "http://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=" + key
    json_response = requests.get(get_weather).json()
    json_response = "আবহাওয়া পূর্বাভাস ( " + city + " )\n" +\
                    "`আবহাওয়ার ধরণ :` " + json_response['weather'][0]['main'] + " (" + json_response['weather'][0]['description'] + ")\n" + \
                    "`তাপমাত্রা : `" + "{:.2f}".format(json_response['main']['temp'] - 273.16) + "°C\n"\
                    + "`বায়ুচাপ :` " + "{:.3f}".format(json_response['main']['pressure']*0.0009869233) + "atm\n"\
                    + "`আর্দ্রতা :` " + str(json_response['main']['humidity']) + "%"
    return json_response


def show_news():
    page = requests.get("https://www.prothomalo.com/")

    tree = html.fromstring(page.content)

    news = tree.xpath('/html/body/div[1]/div[9]/div[2]/div/div/div/div[1]/div/div[1]/div[1]/div[2]/h2/a/text()')[0] \
           + "\n" + "`" + tree.xpath('/html/body/div[1]/div[9]/div[2]/div/div/div/div[1]/div/div[1]/div[1]/div[2]/p/a/text()')[0] + "`"

    return news


def send_updates():
    telegram_bot_sendtext(show_weather('bogra'))
    telegram_bot_sendtext(show_news())


def scheduled_update():
    while True:
        send_updates()
        sleep(300)


@bot.message_handler(commands=['start'])
def start(message):
    global chat_id
    chat_id = message.chat.id
    bot.reply_to(message, 'Hello, ' + message.from_user.first_name + "\n Welcome!")
    Thread(target=scheduled_update).start()


@bot.message_handler(commands=['updates'])
def updates():
    send_updates()


@server.route('/' + TOKEN, methods=['POST'])
def get_message():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://telegram-msg-bot.herokuapp.com/' + TOKEN)
    return "!", 200


server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

