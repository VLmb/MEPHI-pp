import telebot
from gradio_client import Client
from bot.config import TOKEN, SYSTEM_PROMPT, RADIO, API_NAME


bot = telebot.TeleBot(TOKEN)

client = Client("Qwen/Qwen2.5")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message,
                 '''Привет! Я бот, который отправляет
ваши запросы в нейросеть. Напишите мне сообщение, и я отправлю его на обработку.
''')

@bot.message_handler(func=lambda message: True)
def process_user_message(message):
    user_prompt = message.text

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

        bot.reply_to(message, text_answer)

    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка при обработке запроса: {e}")
