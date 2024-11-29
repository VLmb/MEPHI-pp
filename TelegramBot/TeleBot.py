import telebot
import sqlite3
from telebot import types
from telebot.apihelper import send_message

# from module import func



bot = telebot.TeleBot('7691297714:AAG6Z9I7WXtbnqvGOGI1h3Qzfgh_d_70fnk')
name = ''

# state = {}
#
# state = {
#     123434324: {
#         'language': 'Python',
#         'level': 'Senior',
#         'suggestions': '...'
#     }
# }
# state[user_id] = {}
# state[user_id]['language'] = chosen_language
# state[user_id]['level'] = chosen_level
# state[user_id]['language'] =



@bot.message_handler(commands=['start'])
def baza(mes_baz):
    conn = sqlite3.connect('course.sql')
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), luguage varchar(50))')
    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(mes_baz.chat.id, 'Привет сейчас начнем составлять твою анкету! Введите ваше имя')
    bot.register_next_step_handler(mes_baz, user_name)

def user_name(massage):
    global name
    name = massage.text.strip()
    bot.send_message(massage.chat.id, 'введите язык')
    bot.register_next_step_handler(massage, luguage)

def luguage(message):
    yaz = message.text.strip()

    conn = sqlite3.connect('course.sql')
    cur = conn.cursor()

    cur.execute('INSERT INTO users (name, luguage) VALUES ("%s","%s")' % (name, yaz))

    conn.commit()
    cur.close()
    conn.close()


    markup = types.InlineKeyboardMarkup()
    bt1 = types.InlineKeyboardButton('Посмотреть анкету', callback_data='users')
    markup.row(bt1)
    bot.send_message(message.chat.id,'Ваша анкета готова!',reply_markup=markup)

@bot.callback_query_handler(func=lambda callback: True)
def data(call):
    conn = sqlite3.connect('course.sql')
    cur = conn.cursor()

    cur.execute('SELECT * FROM users')
    users = cur.fetchall()

    info= ''
    for el in users:
        info+=f'имя: {el[1]}\n Язык:{el[2]}\n'

    cur.close()
    conn.close()

    bot.send_message(call.message.chat.id, info)


bot.polling(none_stop=True)