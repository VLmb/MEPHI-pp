TOKEN = ""

with open("Skills.txt", "r", encoding="utf-8") as skills:
    SKILLS = skills.readline()


SYSTEM_PROMPT = f'''Ты ассистент, который помогает развиваться IT сотрудникам. 
Напиши навыки, которые необходимо прокачать сотруднику на основе его входной анкеты.
Давай ответы в следующем формате: 'Навыки: '.
Каждую выделенную причину пиши через ; и переход на новую строку. в ответе указывай исключительно финальные навыки.
не указывай ничего, кроме навыков. Ни слова поддержки. ничего более
вот навыки, которые ты можешь использовать в ответе, от себя навыков не добавляй:
{SKILLS}
'''

RADIO = "72B"
API_NAME = "/model_chat"