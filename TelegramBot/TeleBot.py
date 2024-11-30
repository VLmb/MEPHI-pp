import telebot
from telebot import types
from telebot.apihelper import send_message
bot = telebot.TeleBot('7691297714:AAG6Z9I7WXtbnqvGOGI1h3Qzfgh_d_70fnk')

language = ''
level = ''
wishes = ''
@bot.message_handler(content_types=['text'])
def start(message):

    markup = types.ReplyKeyboardMarkup()
    bt1 = types.KeyboardButton('python')
    bt2 = types.KeyboardButton('java')
    bt3 = types.KeyboardButton('C++')
    markup.row(bt1, bt2, bt3)

    if message.text == '/reg':
        bot.send_message(message.from_user.id, "Какой язык ты бы хотел изучить?", reply_markup=markup)
        bot.register_next_step_handler(message, get_language) #следующий шаг – функция get_name
    else:
        bot.send_message(message.from_user.id, 'Привет, я бот который помогает айти сотрудникам улучшать свои навыки! Если ты хочешь стать лучше нужно составить твою анкету, для этого напиши  /reg')

def get_language(message): #получаем фамилию

    markup = types.ReplyKeyboardMarkup()
    bt1 = types.KeyboardButton('Junior')
    bt2 = types.KeyboardButton('Middle')
    bt3 = types.KeyboardButton('Senior')
    markup.row(bt1, bt2, bt3)

    global language
    language = message.text
    bot.send_message(message.from_user.id, 'Выберете ваш уровень программирования!', reply_markup=markup)
    bot.register_next_step_handler(message, get_level)

def get_level(message):
    global level
    level = message.text
    bot.send_message(message.from_user.id,'Теперь напиши свои пожелания по обучению!')
    bot.register_next_step_handler(message, get_wishes)

def get_wishes(message):

    markup = types.ReplyKeyboardMarkup()
    bt1 = types.KeyboardButton('Да')
    bt2 = types.KeyboardButton('Нет')
    markup.row(bt1, bt2)

    global wishes
    wishes = message.text
    bot.send_message(message.from_user.id, 'Вот твоя анкета\n Язык программирования: ' + language + '\n Уровень программирования: ' + level + '\n пожелания: '+wishes+'')
    bot.send_message(message.from_user.id, 'Все верно?', reply_markup=markup)
    bot.register_next_step_handler(message, get_feedback)


def get_feedback(message):
    if message.text == 'Да':
        bot.send_message(message.from_user.id, "Тогда сейчас вышлю тебе несколько курсов")
    else:
        bot.send_message(message.from_user.id, "Чтобы ты хотел изменить?")

