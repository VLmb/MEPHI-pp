import telebot
from telebot import types
from dotenv import load_dotenv
import os

from model import get_course_recommendations, format_course_response

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)

user_data = {}


@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/recommendation':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        buttons = ['Python', 'Java', 'C++']
        markup.add(*[types.KeyboardButton(text) for text in buttons])
        bot.send_message(message.from_user.id, "Какой язык ты бы хотел изучить?", reply_markup=markup)
        bot.register_next_step_handler(message, get_language)
    else:
        bot.send_message(
            message.from_user.id,
            'Привет, я бот, который помогает IT сотрудникам улучшать свои навыки! \n'
            'Если ты хочешь стать лучше, напиши /recommendation для составления анкеты.',
        )

@bot.message_handler(content_types=['text'])
def get_language(message):
    if message.text == 'Python' or message.text == 'Java' or message.text == 'C++':
        user_data['language'] = message.text

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        buttons = ['Junior', 'Middle', 'Senior']
        markup.add(*[types.KeyboardButton(text) for text in buttons])
        bot.send_message(message.from_user.id, 'Выберите ваш уровень программирования!', reply_markup=markup)
        bot.register_next_step_handler(message, get_level)
    else:
        bot.send_message(message.from_user.id, 'Выберете ваш язык программирования, нажав на встроенную кнопку')
        bot.register_next_step_handler(message, get_language)

@bot.message_handler(content_types=['text'])
def get_level(message):
    if message.text == 'Junior' or message.text == 'Middle' or message.text == 'Senior':
        user_data['level'] = message.text

        bot.send_message(message.from_user.id, 'Теперь напишите свои пожелания по обучению!')
        bot.register_next_step_handler(message, get_wishes)
    else:
        bot.send_message(message.from_user.id, 'Выберете ваш уровень программирования, нажав на встроенную кнопку')
        bot.register_next_step_handler(message, get_level)


def get_wishes(message):
    user_data['wishes'] = message.text

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    buttons = ['Да', 'Нет']
    markup.add(*[types.KeyboardButton(text) for text in buttons])

    summary = (
        f"Вот твоя анкета:\n"
        f"Язык программирования: {user_data['language']}\n"
        f"Уровень программирования: {user_data['level']}\n"
        f"Пожелания: {user_data['wishes']}"
    )
    bot.send_message(message.from_user.id, summary)
    bot.send_message(message.from_user.id, 'Все верно?', reply_markup=markup)
    bot.register_next_step_handler(message, get_feedback)


def get_feedback(message):
    if message.text == 'Да':
        recommended_courses = get_course_recommendations(user_data)
        bot_recommendation_message = format_course_response(recommended_courses)
        bot.send_message(message.from_user.id, bot_recommendation_message, parse_mode='HTML')
    if message.text == 'Нет':
        bot.send_message(message.from_user.id, 'Тогда давай заполним анкету заново! Напиши /recommendation')

if __name__ == '__main__':
    bot.polling(none_stop=False, interval=0)
