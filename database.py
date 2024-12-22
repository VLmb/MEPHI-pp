import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker


#Общие данные
dataBaseName = 'Courses'
file_path = 'DataBase/Courses.xlsx'

# Создаем базу данных SQLite и подключаемся к ней
engine = create_engine(f'sqlite:///{dataBaseName}.db')
Base = declarative_base()

# Определяем таблицу Courses
class Course(Base):
    __tablename__ = 'Courses'
    ID = Column(Integer, primary_key=True)
    Name = Column(String)
    Description = Column(String)
    Link = Column(String)
    Duration  = Column(String)
    Cost = Column(String)
    Skills = Column(String)

# Создаем таблицу в базе данных
Base.metadata.create_all(engine)


def parse_excel_to_db():
    '''
    Ничего не принимает и не возвращает, задача функции - занести все поля с
    таблицы в Excel, расположенной по адресу "file_path", в базу данных
    '''
    df = pd.read_excel(file_path)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Добавляем данные из таблицы Excel в базу данных
    for index, row in df.iterrows():
        existing_course = session.query(Course).filter_by(ID=row['ID']).first()
        if not existing_course:
            course = Course(
                ID=row['ID'],
                Name=row['Name'],
                Description=row['Description'],
                Cost=row['Cost'],
                Link=row['Link'],
                Duration=row['Duration'],
                Skills=row['Skills'],
            )
            session.add(course)

    session.commit()
    session.close()

# Функция для проверки совпадений слов в поле Skills
def skill_match(skills_list: list) -> dict[Column[int], int]:
    '''
    Ищет кол-во совпадений требуемых навыков с навыками каждого курса
    :param skills_list: строка с требуемыми навыками, формат: "Навыки: skill1, skill2, ..."
    :return: словарь, в к-ом ключом выступает id курса, а значением - кол-во совпадений
            навыков, которые развивает курс с требуемыми навыками.
    '''
    Session = sessionmaker(bind=engine)
    session = Session()

    courses = session.query(Course).all()

    results = dict()

    for course in courses:
        skills = course.Skills.replace('Навыки: ', '', 1).split(', ')
        matches = sum(1 for skill in skills if skill in skills_list)
        results[course.ID] = matches

    session.close()
    return results

# Запускаем
def main_data(skills_list: list, n: int) ->  list[dict[str, str]]:
    '''
    Основная функция, которая запускает работу базы данных
    :param skills_list: строка с требуемыми навыками, формат: "Навыки: skill1, skill2, ..."
    :param n: кол-во курсов, необходимых для отправки пользователю
    :return: массив словарей полученный в функции "formatting"
    '''
    # Парсим таблицу Excel в базу данных
    parse_excel_to_db()

    # Список строк для проверки совпадений
    #skills_list = ['Golang', 'Machine Learning', 'Coding', "Programming"]

    # Проверяем совпадения
    results = skill_match(skills_list)

    #Имена курсов в список в порядке убывания кол-ва совпадений
    id_list = [key for key, value in sorted(results.items(), key=lambda item: item[1], reverse=True)][:n]

    toTeleBot = formatting(id_list)

    #Передаем данные другому модулю
    return toTeleBot

def formatting(id_list: list) -> list[dict[str, str]]:
    '''
    Формирует массив словарей для передачи данных из бд другому модулю
    :param id_list: массив с id самых релевантных курсов в порядке убывания релевантности
    :return: массив словарей
    '''
    Session = sessionmaker(bind=engine)
    session = Session()
    toTeleBot = []
    for course_id in id_list:
        course = session.query(Course).filter(Course.ID == course_id).first()
        d = dict()
        d['name'] = course.Name.replace('\n', '')
        d['description'] = course.Description.replace('\n', '')
        d['link'] = course.Link.replace('\n', '')
        d['duration'] = course.Duration.replace('\n', '')
        d['cost'] = course.Cost.replace('\n', '')
        toTeleBot.append(d)
    session.close()
    return toTeleBot

if __name__ == '__main__':
    slist = "Go, Programming Basics, Problem Solving, Code Writing, Go Syntax, Basic Programming Concepts, Code Reading, Problem Solving".split(', ')
    print(main_data(slist, 3))

