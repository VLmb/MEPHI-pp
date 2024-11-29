from gradio_client import Client
import pandas as pd

def ai_parsing(description):
    client = Client("Qwen/Qwen2.5")

    system_prompt = '''Ты ассистент, который помогает развиваться IT сотрудникам.
    Выдели ключевые навыки, которые позволяет развивать курс исходя из его описания.
    Дай ответ в формате: 'Навыки:'
    Каждый навык пиши с большой буквы и на английском разделяй их запятыми.
    '''
    user_prompt = f"Пиши кратко, без использования списков. Напиши навыки, которые развивает данный IT курс исходя из его описания: {description}"

    try:
        result = client.predict(
            query=user_prompt,
            history=[],
            system=system_prompt,
            radio="32B",
            api_name="/model_chat"
        )
        if isinstance(result, tuple):
            text_answer = result[1][0][-1]['text']
        else:
            text_answer = result
        return text_answer
    except Exception as e:
        print(f"Error processing description: {description}")
        print(f"Exception: {e}")
        return "Error"

file_path = 'coursesGo.xlsx'
df = pd.read_excel(file_path)

def text(row):
    return ai_parsing(row['Description'])

df['Skills'] = df.apply(text, axis=1)

# Сохраняем обновленный DataFrame обратно в Excel
output_file_path = 'coursesGo_updated.xlsx'
df.to_excel(output_file_path, index=False)

