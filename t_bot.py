import telebot
from config import val, crypto, config
from exception import Convertor, APIException

TOKEN = config['token']
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def comm(message):
    a = message.chat.username
    if a == None:
        bot.send_message(message.chat.id,'Приветствую, Безымянный!\nЯ умею конвертировать валюту.\n '
                                         'Для этого Вам необходимо ввести данные следующим образом:\n '
                                         '<название валюты, цену которой хотите узнать> <пробел> '
                                         '<имя валюты, в которой надо узнать цену первой валюты> <пробел> '
                                         '<количество первой валюты>.\n'
                                         'Пример: BTC USD 10\n'
                                         'Для того, чтобы узнать список доступных валют введите команду: /values')

    else:
        bot.send_message(message.chat.id, f"Приветствую, {a}!\nЯ умею конвертировать валюту.\n"
                                        f"Для этого Вам необходимо ввести данные следующим образом:\n <название валюты, цену которой хотите узнать> <пробел>"
                                        f"<имя валюты, в которой надо узнать цену первой валюты> <пробел> <количество первой валюты>.\n"
                                        f"Пример: BTC USD 10\n"
                                        f"Для того, чтобы узнать список доступных валют введите команду: /values")

@bot.message_handler(commands=['values'])
def com_values(message: telebot.types.Message):
    spisok = []
    for key, value in val.items():
        spisok.append(key+' - '+value)
    otvet = '\n'.join(spisok)
    spisok_cry = []
    for key, value in crypto.items():
        spisok_cry.append(key+' - '+value)
    otvet_crypto = '\n'.join(spisok_cry)
    bot.send_message(message.chat.id, f'Доступны следующие валюты:\n{otvet}\n\nКриптовалюта(Crypto currency):\n{otvet_crypto}')

@bot.message_handler(content_types = ['text'])
def convertor(message: telebot.types.Message):
    try:
        values = message.text.split()
        if len(values) != 3:
            raise APIException('Неправильное количество аргументов')
        base, quote, amo = message.text.split()
        amount = amo.replace(',','.')

        itog = Convertor.get_price(base, quote, amount)
    except APIException as e:
        bot.send_message(message.chat.id, f'Ошибка пользователя:\n{e}')
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка сервера:\n{e}')
    else:
        bot.send_message(message.chat.id, f'Цена {amount} {base} в {quote} = {itog}')

bot.polling(none_stop=True)  # запуск постоянной работы