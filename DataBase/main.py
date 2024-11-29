import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

#Общие данные
dataBaseName = 'Courses'
file_path = '../coursesGo_updated.xlsx'

# Создаем базу данных SQLite и подключаемся к ней
engine = create_engine(f'sqlite:///{dataBaseName}.db')
Base = declarative_base()

# Определяем таблицу Courses
class Course(Base):
    __tablename__ = 'Courses'
    ID = Column(Integer, primary_key=True)
    Name = Column(String)
    Description = Column(String)
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
        results[course.Name] = matches

    session.close()
    return results

# Запускаем
if __name__ == "__main__":

    # Парсим таблицу Excel в базу данных
    parse_excel_to_db()

    # Список строк для проверки совпадений
    skills_list = ['Golang', 'Machine Learning', 'Coding', "Programming"]

    # Проверяем совпадения
    results = check_skills_matches(skills_list)

    #Имена курсов в список в порядке убывания кол-ва совпадений
    ans = [key for key, value in sorted(results.items(), key=lambda item: item[1], reverse=True)]

    #Передаем данные другому модулю
    print(results)
    print(ans)



