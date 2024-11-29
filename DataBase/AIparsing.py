from gradio_client import Client
import pandas as pd

def ai_parsing(description):
    client = Client("Qwen/Qwen2.5")

    system_prompt = '''Ты ассистент, который помогает развиваться IT сотрудникам.
    Выдели ключевые навыки, которые позволяет развивать курс исходя из его описания, также сформируй оптимальное название курса.
    Определи среднюю длительность прохождения данного курса в часах. Все, кроме навыков, сделай на русском.
    Дай ответ в формате: 
    'Навыки:
     Название:
     Длительность:'
    Каждый навык пиши с большой буквы и на английском разделяй их запятыми.
    '''
    user_prompt = f"Пиши кратко, без использования списков. Напиши навыки, которые развивает данный IT курс исходя из его описания, а также оптимальное название и длительность его выполнения: {description}"

    try:
        result = client.predict(
            query=user_prompt,
            history=[],
            system=system_prompt,
            radio="72B",
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

def write_to_excel():
    file_path = 'Descriptions.xlsx'
    df = pd.read_excel(file_path)

    if 'Name' not in df.columns:
        df['Name'] = df['Name'].astype(object)
    if 'Duration' not in df.columns:
        df['Duration'] = df['Duration'].astype(object)
    if 'Skills' not in df.columns:
        df['Skills'] = df['Skills'].astype(object)

    for index, row in df.iterrows():
        # Проверяем, заполнены ли колонки 'Name', 'Duration', и 'Skills'
        if pd.notna(row['Name']) and pd.notna(row['Duration']) and pd.notna(row['Skills']):
            continue

        answer = ai_parsing(row['Description']).replace('Название: ', '').replace('Длительность: ', '').replace('Навыки: ', '').split('\n')
        if len(answer) >= 3:
            df.at[index, 'Name'] = answer[1]
            df.at[index, 'Duration'] = answer[2]
            df.at[index, 'Skills'] = answer[0]
        else:
            print(f"Warning: Not enough data for row {index}")

    # Сохраняем обновленный DataFrame обратно в Excel
    output_file_path = 'Descriptions.xlsx'
    df.to_excel(output_file_path, index=False)

    # Сохраняем обновленный DataFrame обратно в Excel
    output_file_path = '../Courses.xlsx'
    df.to_excel(output_file_path, index=False)

