import sqlite3
import vk_api
import config

vk=vk_api.VkApi(token=config.TOKEN)

# Создание БД
def create(name_file):
    # Устанавливаем соединение с базой данных
    conn = sqlite3.connect(f"archive/{name_file}_base.db")
    cur = conn.cursor()

    # Создаем таблицу Users
    cur.execute('''
    CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY,
    vk_id INTEGER
    )
    ''')

    # Сохраняем изменения и закрываем соединение
    conn.commit()
    conn.close()
    print("БД создана!")

# Добавление
def add_user(name_file, vk_id):
    # Устанавливаем соединение с базой данных
    conn = sqlite3.connect(f"archive/{name_file}_base.db")
    cur = conn.cursor()

    # Добавляем нового пользователя
    cur.execute('INSERT INTO Users (vk_id) VALUES (?)', (vk_id,))

    # Сохраняем изменения и закрываем соединение
    conn.commit()
    conn.close()
    print(f"Запись в БВ vk_id-{vk_id} добавлена!")

# Удаление
def del_user(name_file, vk_id):
    # Устанавливаем соединение с базой данных
    conn = sqlite3.connect(f"archive/{name_file}_base.db")
    cur = conn.cursor()

    # Удаляем пользователя
    cur.execute('DELETE FROM Users WHERE vk_id = ?', (vk_id,))

    # Сохраняем изменения и закрываем соединение
    conn.commit()
    conn.close()
    print(f"Запись для {vk_id} в БВ удалена!")

# Поиск (одного)
def search_user(name_file, vk_id):
    # Устанавливаем соединение с базой данных
    conn = sqlite3.connect(f"archive/{name_file}_base.db")
    cur = conn.cursor()

    # Поиск по vk_id
    cur.execute('SELECT vk_id FROM Users WHERE vk_id = ?', (vk_id,))
    check = cur.fetchone()
    if not check:
        print("Пользователя такого нету")
    else:
        print("Пользователь уже есть")
    
    print(f"Поиск пользователя {vk_id} в БД выполнен")
    conn.close()

# Поиск (всех)
def search_all(name_file):
    # Устанавливаем соединение с базой данных
    conn = sqlite3.connect(f"archive/{name_file}_base.db")
    cur = conn.cursor()

    # Поиск по vk_id
    cur.execute('SELECT vk_id FROM Users')
    check = cur.fetchall()
    print(f"Поиск пользователя в БД выполнен")
    conn.close()
    
    return check