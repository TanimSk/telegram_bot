import requests
from lxml import html

def telegram_bot_sendtext(bot_message):
    bot_token = 'bot_token'
    bot_chatID = 'Chat_ID'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    requests.get(send_text)


def show_weather(city):
    key = "KEY"
    get_weather = "http://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=" + key
    json_response = requests.get(get_weather).json()
    json_response = "আবহাওয়া পূর্বাভাস ( " + city + " )\n" +\
                    "`আবহাওয়ার ধরণ :` " + json_response['weather'][0]['main'] + " (" + json_response['weather'][0]['description'] + ")\n" + \
                    "`তাপমাত্রা : `" + "{:.2f}".format(json_response['main']['temp'] - 273.16) + "°C\n"\
                    + "`বায়ুচাপ :` " + "{:.3f}".format(json_response['main']['pressure']*0.0009869233) + "atm\n"\
                    + "`আর্দ্রতা :` " + str(json_response['main']['humidity']) + "%"
    return json_response


def show_news():
    page = requests.get("https://www.jamuna.tv/")

    tree = html.fromstring(page.content)

    news = tree.xpath('/html/body/main/section[1]/article[1]/div/div/h2/a/text()')[0] \
           + "\n" + "`" +tree.xpath('/html/body/main/section[1]/article[1]/div/div/p[2]/text()')[0] + "`"

    return news


telegram_bot_sendtext(show_weather('bogra'))
telegram_bot_sendtext(show_news())
# print(show_weather('bogra'))

