# 1. Создать базу данных registration.db
# 2. Создать таблицу users_data с колонками UserID, Login (TEXT), Password (TEXT), Code (INTEGER)
# 3. Добавить пользователя с данными Ivan, qwer1234, 1234
# 4. Добавить следующий функционал:
# - 1.регистрация нового пользователя (предусмотреть что каждый пользователь имеет уникальный Login)
# - 2.авторизация в системе - Login, Password
# - 3.восстановление пароля по коду (Code) (4-х значное целостное число) с заменой пароля (обязательный
#  ввод Login)
# 5. Позволить пользователю самостоятельно выбрать одно из трех действий используя ввод в консоль,
# через input() введя цифры 1,2,3.
# 6. Поле Code заполняется пользователем при регистрации, не рандомное число.
# 7. Добавить все необходимые проверки и добавить сообщения об успешной операции, ошибках и т.д.
import sqlite3
import re

"""https://habr.com/ru/articles/349860/"""  ##ссылка не ргулярки

data_connect = sqlite3.connect('registration.db')
cursor = data_connect.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS users_data(UserID INTEGER PRIMARY KEY AUTOINCREMENT,
                                                        Login TEXT NOT NULL,
                                                        Password TEXT NOT NULL,
                                                        Code INTEGER);""")

"""Метод добавления нового пользователя"""


def append_user(data_list):
    cursor.execute(f"""INSERT INTO users_data(Login,Password,Code)
                                                VALUES(?,?,?);""", data_list)  ##Добавляет пользователя в таблицу
    data_connect.commit()
    cursor.execute(f"""SELECT * FROM users_data WHERE Login='{data_list[0]}'""")  ##Находит пользователя в таблице
    data_connect.commit()
    user_in_data = cursor.fetchall()
    assert user_in_data[0][1] == data_list[0], (
        "Пользователь не зарегестрирован")  ##Проверяет что пользователь зарегестрирован и данные из списка и в таблице совпадают
    print(f"Пользователь {user_in_data[0][1]} зарегестрирован")


"""Метод установки пароля"""


def set_password():
    password = input("Введите ваш пароль")
    reg = r'[\s]'
    result = re.findall(reg, password)
    if len(password) == 0 or len(result) != 0:  # Не позволяет оставить поле  пароля пустым
        print("Пароль не должен быть пустым")
        return set_password()
    else:
        return password


"""Метод обновления пароля"""


def set_new_password():
    login = input('Введите Ваш логин')
    req_data_user=cursor.execute(f"""SELECT * FROM users_data WHERE Login='{login}'; """)
    info_data_user=req_data_user.fetchall()

    if len(info_data_user) !=0:
        password = input("Введите Ваш новый пароль")
        reg = r'[\s]'  ##Регулярное выражение ищет  наличие пробелов и табуляций
        result = re.findall(reg, password)
        if len(password) > 0 and len(result) == 0:
            try:
                code = int(input("Напишите Ваше кодовое слово"))
                if code== info_data_user[0][3]:
                    cursor.execute(
                    f"""UPDATE users_data SET Password="{password}" WHERE Login="{login.title()}" AND Code={code};""")
                    data_connect.commit()  ##  Попробуй поменять пароль где такой-то логин и такой-то код если все ок, меняет
                    print("Пароль успешно изменен")
                else:
                    print("Введите верное кодовое слово")
                    return set_new_password()
            except:
                print('Проверьте правильность логина и секретного кода')  ##В случае получения ошибки возвращает ввод пароля
                return set_new_password()
        else:
            print("Поле не долно быть пустым или с пробелами")
            return set_new_password()
    else:
        print("Ведите существующий логин")
        return set_new_password()

"""Метод проверки код-слово 4 символа и все цифры"""


def check_code():
    try:
        code = int(input("Введите  КОД ИЗ 4 ЦИФР"))
        if len(str(code)) == 4:
            code = int(code)
            return code
        elif len(str(code)) > 4:
            print("Вы ввели больше символов, попробуйте в следующий раз")
            return check_code()
        elif len(str(code)) < 4:
            print('Вы ввели меньше символов,попробуйте в следующий раз')
            return check_code()
    except (TypeError, ValueError):
        print("Вы ввели не цифры ")
        try:
            code = int(input("Введите  КОД ИЗ 4 ЦИФР"))
            if len(str(code)) == 4:
                code = int(code)
                return code
            elif len(str(code)) > 4:
                print("Вы больше ввели  символов,попробуйте в следующий раз")
                return check_code()
            elif len(str(code)) < 4:
                print('Вы ввели меньше символов,попробуйте в следующий раз')
                return check_code()

        except (TypeError, ValueError):
            print("Вы ввели не цифры, попробуйте в следующий раз")
        return check_code()


"""Метод проверки существующего логина"""


def check_login():
    login = input("Введите ваш уникальный логин(Буквы или цифры)")
    cursor.execute("""SELECT * FROM users_data""")  ##запрашивает всех из БД таблица юсерс_дата
    users_data = cursor.fetchall()
    reg = r'[\W\s]'  ##Регулярное выражение ищет не буквы, не цифры и  наличие пробелов и табуляций
    result = re.findall(reg, login)
    if len(result) == 0 and len(login)!=0:
        print(f"Ваш логин:{login}")
    else:
        print("У вас есть недопустимые символы или пробелы")
        return check_login()
    for i in users_data:  # Делает цикл по всем элементам из таблицы
        login = login.lower()
        if login == i[1].lower():  ##Сверяет есть ли такой логин в таблице уже
            print("Такой логин есть, попробуйте снова")
            return check_login()
        else:
            continue
    return login.title()


"""Регистрация нового пользователя"""


def registration():
    login = check_login()  ##Выясняет существует ли такой логин и если не существует, то записывает его в переменную
    password = set_password()  ##Устанавливаем пароль
    code = check_code()  ##Устанавливаем кодовое слово и проверяем чтобы оно было только цифры и только 4
    data = [login, password, code]
    append_user(data)  ## Добавляем нашего пользователя в БД


"""Авторизация пользователя"""


def auth():
    login = input("Введите Ваш существующий логин ").lower().title()
    print(login)
    password = input("Введите Ваш пароль")
    cursor.execute(
        f"""SELECT * FROM users_data WHERE Login='{login.title()}'""")  ##Собирает информацию из таблицы, с данным логином
    puck = cursor.fetchall()
    if len(puck) == 0:
        print(
            "Такого логина не существует")  ##Если данные не удалось собрать, то перезапускает мето и просит ввести существующий логин
        return auth()
    else:
        if puck[0][1] == login and puck[0][
            2] == password:  ##Если удалсь собрать данные, то сверяет совпадают пароль введеный с паролем из БД
            print("Вы вошли в систему")
        else:
            print(
                "Пароль не верный")  ##Если пароль  не совпадает, то перезапускает метод и сообщает, что пароль не верный
            return auth()


"""Метод начала приложения"""


def enter():
    first = input(
        "Напишите цифру: \n1 - регистрация\n2 - авторизация\n3 - смена пароля\n>>>>>>")  ##Метол первый страницы,выбрать подходящий вариант
    if first == '1':
        registration()
    elif first == '2':
        auth()
    elif first == '3':
        set_new_password()


# append_user(['Ivan','qwer123',1234]) ##Создает Ивана
enter()
# cursor.execute("""DROP TABLE users_data;""")
# data_connect.commit()