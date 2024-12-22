import telebot
from gradio_client import Client
from PP_Neuro_Part.config import TOKEN, SYSTEM_PROMPT, RADIO, API_NAME

bot = telebot.TeleBot(TOKEN)
client = Client("Qwen/Qwen2.5")


def send_welcome(message):
    bot.reply_to(message, '''Привет! Я бот, который отправляет ваши запросы в нейросеть.  
Напишите мне сообщение, и я отправлю его на обработку. ''')


def process_user_message(message):
    user_data = message.text
    skills_list = get_skills_based_on_input(user_data)

    if skills_list:
        response_message = format_skills_response(skills_list)
        bot.reply_to(message, response_message)
    else:
        bot.reply_to(message, "Не удалось получить список навыков.")


def get_skills_based_on_input(user_dict):
    user_prompt = create_user_prompt(user_dict)
    try:
        result = client.predict(
            query=user_prompt,
            system=SYSTEM_PROMPT,
            radio=RADIO,
            api_name=API_NAME
        )
        if isinstance(result, tuple):
            text_answer = result[1][0][-1]['text']
        else:
            text_answer = result

        return parse_skills(text_answer)
    except Exception as e:
        print(e)
        return None


def create_user_prompt(user_dict):
    prompt = f"Подсказать навыки для уровня {user_dict['level']} языка {user_dict['language']}. {user_dict['suggestions']}"
    return prompt


def parse_skills(text_answer):
    skills = []  # Здесь должен быть код, который парсит text_answer и заполняет список skills
    # skills = [{'name': '...', 'description': '...', 'link': '...', 'duration': '...'}, ...]
    return skills


def format_skills_response(skills_list):
    response = "Вот список навыков:\n"
    for skill in skills_list:
        response += f"Название: {skill['name']}\nОписание: {skill['description']}\nСсылка: {skill['link']}\nПродолжительность: {skill['duration']}\n\n"
    return response


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    send_welcome(message)


@bot.message_handler(func=lambda message: True)
def handle_user_message(message):
    process_user_message(message)


bot.polling()
