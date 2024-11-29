import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

#Общие данные
dataBaseName = 'Courses'
file_path = '../Courses.xlsx'

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
    Skills = Column(String)

# Создаем таблицу в базе данных
Base.metadata.create_all(engine)

# Функция для парсинга таблицы Excel в базу данных
def parse_excel_to_db():
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
                Link=row['Link'],
                Duration=row['Duration'],
                Skills=row['Skills'],
            )
            session.add(course)

    session.commit()
    session.close()

# Функция для проверки совпадений слов в поле Skills
def check_skills_matches(skills_list):
    Session = sessionmaker(bind=engine)
    session = Session()

    courses = session.query(Course).all()

    results = dict()

    for course in courses:
        skills = course.Skills.replace('Навыки: ', '', 1).split(', ')
        #print(skills)
        matches = sum(1 for skill in skills if skill in skills_list)
        results[course.ID] = matches

    session.close()
    return results

# Запускаем
def data(skills_list, n):

    # Парсим таблицу Excel в базу данных
    parse_excel_to_db()

    # Список строк для проверки совпадений
    #skills_list = ['Golang', 'Machine Learning', 'Coding', "Programming"]

    # Проверяем совпадения
    results = check_skills_matches(skills_list)

    #Имена курсов в список в порядке убывания кол-ва совпадений
    id_list = [key for key, value in sorted(results.items(), key=lambda item: item[1], reverse=True)][:n]

    #Передаем данные другому модулю
    return send_to_bot(id_list, n)

def send_to_bot(id_list):
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
        toTeleBot.append(d)
    session.close()
    return toTeleBot

slist = "Go, Programming Basics, Problem Solving, Code Writing, Go Syntax, Basic Programming Concepts, Code Reading, Problem Solving".split(', ')
print(data(slist, 2))


