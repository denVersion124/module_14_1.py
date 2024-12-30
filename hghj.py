import os
import sqlite3

# Удалите файл базы данных, если он существует
db_file = 'not_telegram.db'
if os.path.exists(db_file):
    os.remove(db_file)

try:
    # Подключаемся к базе данных и создаем курсор
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Создаем таблицу Users, если она еще не создана
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            age INTEGER,
            balance INTEGER NOT NULL
        )
    ''')

    # Заполняем таблицу 10 записями через цикл for
    users_data = []
    for i in range(1, 11):
        username = f'User{i}'
        email = f'example{i}@gmail.com'
        age = i * 10  # Возраст 10, 20, ..., 100
        balance = 1000  # Начальный баланс
        users_data.append((username, email, age, balance))

    # Вставляем данные в таблицу
    cursor.executemany('''
        INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)
    ''', users_data)

    # Обновление balance у каждой 2ой записи начиная с 1ой на 500
    cursor.execute('''
        UPDATE Users
        SET balance = 500
        WHERE id % 2 = 1
    ''')

    # Удаление каждой 3ей записи начиная с 1ой
    cursor.execute('''
        DELETE FROM Users
        WHERE (id - 1) % 3 = 0
    ''')

    # Выполняем выборку всех записей, где возраст не равен 60
    cursor.execute('''
        SELECT username, email, age, balance
        FROM Users
        WHERE age != 60
    ''')

    # Получаем все записи
    results = cursor.fetchall()

    # Выводим результаты
    for row in results:
        username, email, age, balance = row
        print(f"Имя: {username} | Почта: {email} | Возраст: | Баланс: {balance}")
  
except sqlite3.DatabaseError as e:
    print(f"Ошибка базы данных: {e}")
except Exception as e:
    print(f"Произошла ошибка: {e}")
finally:
    # Закрываем соединение
    if conn:
        conn.commit()
        conn.close()
