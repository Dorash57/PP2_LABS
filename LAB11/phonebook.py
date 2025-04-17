import csv
import psycopg2

# Параметры базы данных
DataBase = {
    'host': '127.0.0.1',        # адрес сервера БД
    'port': 5432,               # порт PostgreSQL
    'database': 'Dorash',   # имя базы данных
    'user': 'postgres',         # пользователь
    'password': '1689518779'      # пароль
}

# Создание Таблицы
def init_db():
    with psycopg2.connect(**DataBase) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS phonebook (
                    id SERIAL PRIMARY KEY,
                    first_name TEXT NOT NULL,
                    last_name TEXT,
                    phone TEXT UNIQUE NOT NULL
                );
                """
            )
        conn.commit()

#  Добавление данных

def insert_from_csv(csv_path):
    with psycopg2.connect(**DataBase) as conn:
        with conn.cursor() as cur, open(csv_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                cur.execute(
                    "INSERT INTO phonebook (first_name, last_name, phone) VALUES (%s, %s, %s)"
                    " ON CONFLICT (phone) DO NOTHING;",
                    (row['first_name'], row.get('last_name'), row['phone'])
                )
        conn.commit()
    print("Контакты из CSV загружены.")

def insert_console():
    first = input("Имя: ").strip()
    last = input("Фамилия (необязательно): ").strip() or None
    phone = input("Телефон: ").strip()
    with psycopg2.connect(**DataBase) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO phonebook (first_name, last_name, phone) VALUES (%s, %s, %s)",
                (first, last, phone)
            )
        conn.commit()
    print("Контакт добавлен.")

# Обнова

def update_contact():
    criterion = input("Обновить по (1) телефону или (2) id? Введите 1 или 2: ")
    key = input("Введите значение (телефон или id): ").strip()
    field = input("Поле для изменения (first_name, last_name, phone): ")
    new_val = input(f"Новое значение для {field}: ")

    with psycopg2.connect(**DataBase) as conn:
        with conn.cursor() as cur:
            if criterion == '1':
                cur.execute(f"UPDATE phonebook SET {field} = %s WHERE phone = %s", (new_val, key))
            else:
                cur.execute(f"UPDATE phonebook SET {field} = %s WHERE id = %s", (new_val, key))
        conn.commit()
    print("Контакт обновлён.")

# Запрос данных

def query_phonebook():
    print("Фильтры: 1) все  2) по имени  3) по шаблону телефона")
    choice = input("Выберите фильтр: ")
    with psycopg2.connect(**DataBase) as conn:
        with conn.cursor() as cur:
            if choice == '1':
                cur.execute("SELECT * FROM phonebook ORDER BY first_name")
            elif choice == '2':
                name = input("Введите имя для поиска: ").strip()
                cur.execute("SELECT * FROM phonebook WHERE first_name ILIKE %s", (f"%{name}%",))
            else:
                pattern = input("Введите шаблон телефона ").strip()
                cur.execute("SELECT * FROM phonebook WHERE phone LIKE %s", (pattern,))
            rows = cur.fetchall()
            for r in rows:
                print(r)

# Удаление данных

def delete_contact():
    choice = input("Удалить по (1) телефону или (2) имя? ")
    key = input("Введите значение: ").strip()
    with psycopg2.connect(**DataBase) as conn:
        with conn.cursor() as cur:
            if choice == '1':
                cur.execute("DELETE FROM phonebook WHERE phone = %s", (key,))
            else:
                cur.execute("DELETE FROM phonebook WHERE first_name = %s", (key,))
        conn.commit()
    print("Контакт удалён.")

# Поиск по паттерну

def on_pattern():
    pattern = input("Введите паттерн: ").strip()
    with psycopg2.connect(**DataBase) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT * FROM phonebook
                WHERE first_name ILIKE %s OR last_name ILIKE %s OR phone ILIKE %s
            """, (f"%{pattern}%", f"%{pattern}%", f"%{pattern}%"))
            rows = cur.fetchall()
            for r in rows:
                print(r)

# Вставка или обновление

def add_update_contact():
    p_first = input("Имя: ").strip()
    p_last = input("Фамилия (необязательно): ").strip() or None
    p_phone = input("Телефон: ").strip()
    with psycopg2.connect(**DataBase) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                DO $$
                BEGIN
                    IF EXISTS (
                        SELECT 1 FROM phonebook WHERE first_name = %s AND last_name = %s
                    ) THEN
                        UPDATE phonebook SET phone = %s WHERE first_name = %s AND last_name = %s;
                    ELSE
                        INSERT INTO phonebook(first_name, last_name, phone) VALUES (%s, %s, %s);
                    END IF;
                END $$;
            """, (p_first, p_last, p_phone, p_first, p_last, p_first, p_last, p_phone))
        conn.commit()
    print("Контакт обновлён или добавлен.")

# Пагинация

def get_paginated():
    limit = int(input("Сколько записей вывести: "))
    offset = int(input("С какой записи начать: "))
    with psycopg2.connect(**DataBase) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM phonebook ORDER BY id LIMIT %s OFFSET %s", (limit, offset))
            rows = cur.fetchall()
            for r in rows:
                print(r)

# Меню

def main():
    init_db()
    while True:
        print("\n Меню Телефонной книги:")
        print("1. Импорт из CSV")
        print("2. Добавить контакт вручную")
        print("3. Обновить контакт")
        print("4. Поиск контактов")
        print("5. Удалить контакт")
        print("6. Поиск по паттерну")
        print("7. Вставить/Обновить контакт")
        print("8. Пагинация")
        print("0. Выход")
        inp = input("Выберите опцию: ")
        if inp == '1':
            path = input("Путь к CSV-файлу: ")
            insert_from_csv(path)
        elif inp == '2':
            insert_console()
        elif inp == '3':
            update_contact()
        elif inp == '4':
            query_phonebook()
        elif inp == '5':
            delete_contact()
        elif inp == '6':
            on_pattern()
        elif inp == '7':
            add_update_contact()
        elif inp == '8':
            get_paginated()
        elif inp == '0':
            break

if __name__ == '__main__':
    main()