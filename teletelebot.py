import telebot
from config import keys, TOKEN
from extensions import APIException, Converter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Доброго времени суток!\nЧтобы начать работу введите комманду боту в следующем формате:\n\n <имя валюты, цену которой Вы хочет узнать>  \
<имя валюты, в которой надо узнать цену первой валюты> \
 <количество первой валюты> \n\nЧтобы увидеть список всех доступных валют нажимте на: /values или введите в консоль, а если возникнут трудности,\n зовите на помощь, при помощи /help.'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Слишком много параметров.')

        quote, base, amount = values
        total_base = Converter.convert(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'На данный момент цена {amount} {quote} в {base} - составляет {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling()