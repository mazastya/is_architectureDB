from time import sleep

from faker import Faker
import random
from faker.providers.phone_number.ru_RU import Provider as RuPhoneNumberProvider
from faker.generator import random
from faker.providers import BaseProvider
import psycopg2
from psycopg2 import OperationalError

# все будем заполнять на русском
fake = Faker('ru_RU')

'''
создаем подключение
'''

conn = None
while conn == None:
    print("пытаюсь")
    try:
        conn = psycopg2.connect(database="name", host="db", user="postgres", password="postgres")
        print("подключено")
    except OperationalError as e:
        print(f"Ошибка: '{e}'")
        sleep(2)
cursor = conn.cursor()

query = "SELECT COUNT(*) FROM curators;"
cursor.execute(query)
count = cursor.fetchone()[0]
print(count)



'''
Заполняем таблицу для кураторов
'''
query = "SELECT COUNT(*) FROM curators;"
cursor.execute(query)
count = cursor.fetchone()[0]
print(count)

while count < 10000:
    school_number = fake.random_int(min=1, max=1000000)

    school_region = ["Воронежская область", "Тамбовская область", "Ямало-Ненецкий автономный округ",
                     "Московская область", "Приморский край", "Новгородская область"]

    region = fake.random_element(school_region)
    school = f"Школа {school_number}"
    teacher = fake.name()

    query = f"INSERT INTO curators (teacher, school, region) VALUES ('{teacher}', '{school}', '{region}');"
    print(f"добавлено: '{region}', '{school}', '{teacher}'")
    count += 1
    cursor.execute(query)


'''
Заполняем таблицу для команд
'''
query = "SELECT COUNT(*) FROM commands;"
cursor.execute(query)
count = cursor.fetchone()[0]
print(count)


class TeamRoleProvider(BaseProvider):
    def team_role(self):
        roles = ['none',
                 'admin',
                 'teacher',
                 'fundraiser',
                 'manager',
                 'curator',
                 'coordinator',
                 'methodist',
                 'developer']
        return self.random_element(roles)


while count < 10000:
    school_number = fake.random_int(min=1, max=1000000)

    school_region = ["Воронежская область", "Тамбовская область", "Ямало-Ненецкий автономный округ",
                     "Московская область", "Приморский край", "Новгородская область"]

    fake.add_provider(TeamRoleProvider)

    region = fake.random_element(school_region)
    role = fake.team_role()
    school = f"Школа {school_number}"
    teacher = fake.name()

    query = f"INSERT INTO commands (teacher, school, region, role) VALUES ('{teacher}', '{school}', '{region}', '{role}');"
    print(f"добавлено: '{region}', '{school}', '{teacher}', '{role}'")
    count += 1
    cursor.execute(query)

'''
Заполняем таблицу для методистов
'''
query = "SELECT COUNT(*) FROM methodologists;"
cursor.execute(query)
count = cursor.fetchone()[0]
print(count)

while count < 10000:
    school_subjects = ["Математика", "Русский язык", "Литература", "Физика", "Химия", "История", "География",
                       "Биология"]

    name = fake.name()
    subject = fake.random_element(school_subjects)
    teacher = fake.name()

    query = f"INSERT INTO methodologists (name, subject, teacher) VALUES ('{name}', '{subject}', '{teacher}');"
    print(f"добавлено: '{name}', '{subject}', '{teacher}'")
    count += 1
    cursor.execute(query)

'''
Заполняем таблицу для истории донатов
'''
query = "SELECT COUNT(*) FROM history_donate;"
cursor.execute(query)
count = cursor.fetchone()[0]
print(count)

while count < 10000:
    username = fake.name()
    date_donate = fake.date()
    time_donate = fake.time()
    sum_donate = fake.random_int(min=1000, max=10000)

    query = (
        f"INSERT INTO history_donate (username, time_donate, date_donate, sum_donate) VALUES ('{username}', '{time_donate}', '{date_donate}', '{sum_donate}')")
    print(f"добавлено: '{username}', '{time_donate}', '{date_donate}', '{sum_donate}'")
    count += 1
    cursor.execute(query)

'''
Заполняем таблицу для юзеров
'''
query = "SELECT COUNT(*) FROM users;"
cursor.execute(query)
count = cursor.fetchone()[0]
print(count)


class UserRoleProvider(BaseProvider):
    def user_role(self):
        roles = ['none',
                 'user',
                 'donate_user',
                 'candidate']
        return self.random_element(roles)


while count < 10000:

    query = "SELECT * FROM history_donate LIMIT 1;"
    cursor.execute(query)
    min_fk = cursor.fetchone()[0]
    max_fk = min_fk + 999

    fake.add_provider(UserRoleProvider)

    choice_last_name_2 = random.choice([True, False])

    if choice_last_name_2:
        user_lastname = fake.middle_name()
    else:
        user_lastname = None

    user_name = fake.first_name()
    user_surname = fake.last_name()
    donate_history = fake.random_int(min=min_fk, max=max_fk)
    role = fake.user_role()

    query = (
        f"INSERT INTO users (user_name, user_surname, user_lastname, donate_history, role) VALUES ('{user_name}', '{user_surname}', '{user_lastname}', '{donate_history}', '{role}')")
    print(f"добавлено: '{user_name}', '{user_surname}', '{user_lastname}', '{donate_history}', '{role}'")
    count += 1
    cursor.execute(query)

'''
Заполняем таблицу для учителей
'''
query = "SELECT COUNT(*) FROM teachers;"
cursor.execute(query)
count = cursor.fetchone()[0]
print(count)

while count < 10000:

    query = "SELECT * FROM curators LIMIT 1;"
    cursor.execute(query)
    min_fk_curator = cursor.fetchone()[0]
    max_fk_curator = min_fk_curator + 999

    query = "SELECT * FROM users LIMIT 1;"
    cursor.execute(query)
    min_fk_user = cursor.fetchone()[0]
    max_fk_user = min_fk_curator + 999

    choice_last_name_2 = random.choice([True, False])

    if choice_last_name_2:
        teacher_lastname = fake.middle_name()
    else:
        teacher_lastname = None

    fake.add_provider(RuPhoneNumberProvider)

    school_subjects = ["Математика", "Русский язык", "Литература", "Физика", "Химия", "История", "География",
                       "Биология"]

    school_region = ["Воронежская область", "Тамбовская область", "Ямало-Ненецкий автономный округ",
                     "Московская область", "Приморский край", "Новгородская область"]

    school_number = fake.random_int(min=1, max=1)

    teacher_name = fake.first_name()
    teacher_surname = fake.last_name()
    phone_number = fake.phone_number()
    subject = fake.random_element(school_subjects)
    region = fake.random_element(school_region)
    school = f"Школа {school_number}"
    graduate = random.choice([True, False])
    curator_id = fake.random_int(min=min_fk_curator, max=max_fk_curator)
    user_id = fake.random_int(min=min_fk_user, max=max_fk_user)

    query = (
        f"INSERT INTO teachers (teacher_name, teacher_surname, teacher_lastname, phone_number, subject, region, school, graduate, curator_id, user_id) "
        f"VALUES ('{teacher_name}', '{teacher_surname}', '{teacher_lastname}', '{phone_number}', '{subject}','{region}', '{school}', '{graduate}', '{curator_id}', '{user_id}')")
    print(
        f"добавлено: '{teacher_name}', '{teacher_surname}', '{teacher_lastname}', '{phone_number}', '{subject}', '{region}', '{school}', '{graduate}', '{curator_id}', '{user_id}'")
    count += 1
    cursor.execute(query)


'''
Заполняем таблицу для школ
'''
query = "SELECT COUNT(*) FROM schools;"
cursor.execute(query)
count = cursor.fetchone()[0]
print(count)

while count < 10000:

    query = "SELECT * FROM teachers LIMIT 1;"
    cursor.execute(query)
    min_fk_teacher = cursor.fetchone()[0]
    max_fk_teacher = min_fk_teacher + 999

    school_number = fake.random_int(min=1, max=999)

    school_region = ["Воронежская область", "Тамбовская область", "Ямало-Ненецкий автономный округ",
                     "Московская область", "Приморский край", "Новгородская область"]


    region = fake.random_element(school_region)
    name = f"Школа {school_number}"
    teacher_id = fake.random_int(min=min_fk_teacher, max=max_fk_teacher)

    query = f"INSERT INTO schools (teacher_id, name, region) VALUES ('{teacher_id}', '{name}', '{region}');"
    print(f"добавлено: '{teacher_id}', '{name}', '{region}'")
    count += 1
    cursor.execute(query)


'''
Заполняем таблицу для регионов
'''
query = "SELECT COUNT(*) FROM regions;"
cursor.execute(query)
count = cursor.fetchone()[0]
print(count)

while count < 10000:

    query = "SELECT * FROM teachers LIMIT 1;"
    cursor.execute(query)
    min_fk_teacher = cursor.fetchone()[0]
    max_fk_teacher = min_fk_teacher + 999

    query = "SELECT * FROM commands LIMIT 1;"
    cursor.execute(query)
    min_fk_commands = cursor.fetchone()[0]
    max_fk_commands = min_fk_commands + 999

    school_region = ["Воронежская область", "Тамбовская область", "Ямало-Ненецкий автономный округ",
                "Московская область", "Приморский край", "Новгородская область"]


    school_number = fake.random_int(min=1, max=999)

    school = f"Школа {school_number}"
    name = fake.random_element(school_region)
    teacher_id = fake.random_int(min=min_fk_teacher, max=max_fk_teacher)
    command_id = fake.random_int(min=min_fk_commands, max=max_fk_commands)

    query = f"INSERT INTO regions (name, teacher_id, command_id, school) VALUES ('{name}', '{teacher_id}', '{command_id}', '{school}');"
    print(f"добавлено: '{name}', '{teacher_id}', '{command_id}', '{school}'")
    count += 1
    cursor.execute(query)


'''
Заполняем таблицу для кандидатов
'''
query = "SELECT COUNT(*) FROM candidates;"
cursor.execute(query)
count = cursor.fetchone()[0]
print(count)

while count < 10000:

    choice_last_name_2 = random.choice([True, False])

    if choice_last_name_2:
        candidate_lastname = fake.middle_name()
    else:
        candidate_lastname = None

    fake.add_provider(RuPhoneNumberProvider)

    school_subjects = ["Математика", "Русский язык", "Литература", "Физика", "Химия", "История", "География",
                       "Биология"]

    school_region = ["Воронежская область", "Тамбовская область", "Ямало-Ненецкий автономный округ",
                     "Московская область", "Приморский край", "Новгородская область"]

    universities = [
        "Московский государственный университет имени М.В. Ломоносова",
        "Санкт-Петербургский государственный университет",
        "Новосибирский государственный университет",
        "Казанский (Приволжский) федеральный университет",
        "Уральский федеральный университет",
        "Сибирский федеральный университет",
        "Российская экономическая академия имени Г.В. Плеханова",
        "Санкт-Петербургский политехнический университет Петра Великого",
        "Московский физико-технический институт",
        "Иркутский государственный университет",
        "Национальный исследовательский университет «Высшая школа экономики»",
        "Томский политехнический университет",
        "Красноярский федеральный университет",
        "Санкт-Петербургский горный университет",
        "Российский государственный гуманитарный университет",
        "Кемеровский государственный университет",
        "Московский институт стали и сплавов",
        "Университет ИТМО в Санкт-Петербурге",
        "Российский университет дружбы народов",
        "Дальневосточный федеральный университет"
    ]

    school_number = fake.random_int(min=1, max=999)

    candidate_name = fake.first_name()
    candidate_surname = fake.last_name()
    desired_region = fake.random_element(school_region)
    phone_number = fake.phone_number()
    education_received = fake.random_element(universities)
    selection_passed = random.choice([True, False])
    desired_subject = fake.random_element(school_subjects)

    query = (
        f"INSERT INTO candidates (candidate_name, candidate_surname, candidate_lastname, desired_region, phone_number, education_received, selection_passed, desired_subject) "
        f"VALUES ('{candidate_name}', '{candidate_surname}', '{candidate_lastname}', '{desired_region}', '{phone_number}','{education_received}', '{selection_passed}', '{desired_subject}')")
    print(
        f"добавлено: '{candidate_name}', '{candidate_surname}', '{candidate_lastname}', '{desired_region}', '{phone_number}', '{education_received}', '{selection_passed}', '{desired_subject}'")
    count += 1
    cursor.execute(query)

'''
Заполняем таблицу many-to-many учитель - школа
'''
query = "SELECT COUNT(*) FROM teachers_schools;"
cursor.execute(query)
count = cursor.fetchone()[0]
print(count)

while count < 10000:

    query = "SELECT * FROM teachers LIMIT 1;"
    cursor.execute(query)
    min_fk_teacher = cursor.fetchone()[0]
    max_fk_teacher = min_fk_teacher + 999

    query = "SELECT * FROM schools LIMIT 1;"
    cursor.execute(query)
    min_fk_school = cursor.fetchone()[0]
    max_fk_school = min_fk_school + 999

    teacher_id = fake.random_int(min=min_fk_teacher, max=max_fk_teacher)
    school_id = fake.random_int(min=min_fk_school, max=max_fk_school)

    query = f"INSERT INTO teachers_schools (teacher_id, school_id) VALUES ('{teacher_id}', '{school_id}');"
    print(f"добавлено: '{teacher_id}', '{school_id}'")
    count += 1
    cursor.execute(query)

'''
Заполняем таблицу many-to-many команда - куратор
'''
query = "SELECT COUNT(*) FROM commands_curators;"
cursor.execute(query)
count = cursor.fetchone()[0]
print(count)

while count < 10000:

    query = "SELECT * FROM commands LIMIT 1;"
    cursor.execute(query)
    min_fk_commands = cursor.fetchone()[0]
    max_fk_commands = min_fk_commands + 999

    query = "SELECT * FROM curators LIMIT 1;"
    cursor.execute(query)
    min_fk_curator = cursor.fetchone()[0]
    max_fk_curator = min_fk_curator + 999

    command_id = fake.random_int(min=min_fk_commands, max=max_fk_commands)
    curator_id = fake.random_int(min=min_fk_curator, max=max_fk_curator)

    query = f"INSERT INTO commands_curators (command_id, curator_id) VALUES ('{command_id}', '{curator_id}');"
    print(f"добавлено: '{command_id}', '{curator_id}'")
    count += 1
    cursor.execute(query)


'''
Заполняем таблицу many-to-many методист - учитель
'''
query = "SELECT COUNT(*) FROM methodists_teachers;"
cursor.execute(query)
count = cursor.fetchone()[0]
print(count)

while count < 10000:

    query = "SELECT * FROM methodologists LIMIT 1;"
    cursor.execute(query)
    min_fk_methodist = cursor.fetchone()[0]
    max_fk_methodist = min_fk_methodist + 999

    query = "SELECT * FROM teachers LIMIT 1;"
    cursor.execute(query)
    min_fk_teacher = cursor.fetchone()[0]
    max_fk_teacher = min_fk_teacher + 999

    methodologist_id = fake.random_int(min=min_fk_methodist, max=max_fk_methodist)
    teacher_id = fake.random_int(min=min_fk_teacher, max=max_fk_teacher)

    query = f"INSERT INTO methodists_teachers (methodologist_id, teacher_id) VALUES ('{methodologist_id}', '{teacher_id}');"
    print(f"добавлено: '{methodologist_id}', '{teacher_id}'")
    count += 1
    cursor.execute(query)

'''
Заполняем таблицу many-to-many регион - школа
'''
query = "SELECT COUNT(*) FROM regions_schools;"
cursor.execute(query)
count = cursor.fetchone()[0]
print(count)

while count < 10000:

    query = "SELECT * FROM regions LIMIT 1;"
    cursor.execute(query)
    min_fk_region = cursor.fetchone()[0]
    max_fk_region = min_fk_region + 999

    query = "SELECT * FROM schools LIMIT 1;"
    cursor.execute(query)
    min_fk_school = cursor.fetchone()[0]
    max_fk_school = min_fk_school + 999

    region_id = fake.random_int(min=min_fk_region, max=max_fk_region)
    school_id = fake.random_int(min=min_fk_school, max=max_fk_school)

    query = f"INSERT INTO regions_schools (region_id, school_id) VALUES ('{region_id}', '{school_id}');"
    print(f"добавлено: '{region_id}', '{school_id}'")
    count += 1
    cursor.execute(query)


'''
Заполняем таблицу many-to-many история донатов - юзер
'''
query = "SELECT COUNT(*) FROM history_donate_donate_users;"
cursor.execute(query)
count = cursor.fetchone()[0]
print(count)

while count < 10000:

    query = "SELECT * FROM history_donate LIMIT 1;"
    cursor.execute(query)
    min_fk_history_donate = cursor.fetchone()[0]
    max_fk_history_donate = min_fk_history_donate + 999

    query = "SELECT * FROM users LIMIT 1;"
    cursor.execute(query)
    min_fk_user = cursor.fetchone()[0]
    max_fk_user = min_fk_user + 999

    history_donate_id = fake.random_int(min=min_fk_history_donate, max=max_fk_history_donate)
    user_id = fake.random_int(min=min_fk_user, max=max_fk_user)

    query = f"INSERT INTO history_donate_donate_users (history_donate_id, user_id) VALUES ('{history_donate_id}', '{user_id}');"
    print(f"добавлено: '{history_donate_id}', '{user_id}'")
    count += 1
    cursor.execute(query)

query = "INSERT INTO teachers_partitioned_by_region SELECT * FROM teachers;"
cursor.execute(query)

query = "INSERT INTO teachers_partitioned_by_subject SELECT * FROM teachers;"
cursor.execute(query)

conn.commit()
cursor.close()
conn.close()
