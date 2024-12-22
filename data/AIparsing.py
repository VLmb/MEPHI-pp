from gradio_client import Client
import pandas as pd

def ai_parsing(description: str) -> str:
    '''
    Отправляет запрос нейросети
    :param description: описание курса
    :return:
    '''
    client = Client("Qwen/Qwen2.5")

    system_prompt = '''Ты ассистент, который помогает развиваться IT сотрудникам.
    Тебе дают описание IT курса из интернета, ты должен проанализировать его и сделать следующее:
    1. сформировать оптимальное название для этого курса
    2. выделить ключевые навыки, которые развивает данный курс(не больше десяти)
    3. определить примерную длительность прохождения курса в часах
    4. переписать его описание так, чтобы оно было максимально информативным и вмещалось в 5-10 предложений
    Все, кроме навыков, сделай на русском.
    Дай ответ в формате: 
    'Название:
     Навыки:
     Длительность:
     Описание:'
    Каждый навык пиши с большой буквы и на английском, разделяй их запятыми.
    '''
    user_prompt = f"Пиши кратко, без использования списков. Напиши навыки, которые развивает данный IT курс исходя из его описания, а также оптимальное название, длительность его выполнения и перепиши описание, чтобы оно было информативным и кратким: {description}"

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
    '''
    записывает полученный от нейросети ответ в таблицу Excel
    :return: nothing
    '''
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
        answer = ai_parsing(row['Description']).replace('Название: ', '').replace('Навыки: ', '').replace('Длительность: ', '').replace('Описание: ', '').split('\n')
        i = 0
        while i < len(answer):
            if answer[i] == '':
                answer.pop(i)
            i+=1
        if len(answer) >= 4:
            df.at[index, 'Name'] = answer[0]
            df.at[index, 'Skills'] = answer[1]
            df.at[index, 'Duration'] = answer[2]
            df.at[index, 'Description'] = answer[3]
        else:
            print(f"Warning: Not enough data for row {index}")

    # Сохраняем обновленный DataFrame обратно в Excel
    output_file_path = 'Courses.xlsx'
    df.to_excel(output_file_path, index=False)


if __name__ == '__main__':
    write_to_excel()