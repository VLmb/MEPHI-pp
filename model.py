import telebot
from gradio_client import Client

from database import main_data

client = Client("Qwen/Qwen2.5")

with open("data/Skills.txt", "r", encoding="utf-8") as skills:
    SKILLS = skills.readline()


SYSTEM_PROMPT = f'''Ты ассистент, который помогает развиваться IT сотрудникам. 
Напиши навыки, которые необходимо прокачать сотруднику на основе его входной анкеты.
Давай ответы в следующем формате: 'Навыки:'. Пример ответа: 'Навыки: Python Syntax; Arrays; Web Development;'
Каждую выделенный навык пиши через ; и переход на новую строку. В ответе указывай исключительно навыки.
Вот навыки, которые ты можешь использовать в ответе, выбери только 5 навыков из списка ниже:
{SKILLS}
'''

RADIO = "72B"
API_NAME = "/model_chat"


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
        print(text_answer)
        return parse_skills(text_answer)
    except Exception as e:
        print(e)
        return None


def create_user_prompt(user_dict):
    prompt = f"Подскажи навыки для развития сотрудника с уровнем {user_dict['level']}, который программирует на языке {user_dict['language']}. Вот предпочтения сотрудника: {user_dict['wishes']}"
    return prompt


def parse_skills(text_answer):
    text_skills = text_answer.split("Навыки:")[1].strip()
    return [x.strip() for x in text_skills.split(';') if x.strip()]


def get_course_recommendations(user_data: dict):
    recommended_skills = get_skills_based_on_input(user_data)
    recommended_courses = main_data(recommended_skills, 3)
    return recommended_courses

def format_course_response(courses_list):
    response = "<b>Вот список рекомендованных курсов для повышения вашей квалификации:</b>\n\n"
    for course in courses_list:
        response += (
            f"<b>{course['name']}</b>\n"
            # f"{course['description']}\n"
            f"<a href=\"{course['link']}\">Ссылка на курс</a>\n"
            f"Стоимость: {course['cost']}\n"
            f"Продолжительность: {course['duration']}\n\n"
        )
    return response

if __name__ == '__main__':
    test_user_data = {'level': 'python',
                      'language': 'Middle',
                      'wishes': 'Хочу изучить python'
                      }
    recommended_courses = get_course_recommendations(test_user_data)
    print(recommended_courses)
    print(format_course_response(recommended_courses))