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
    # Добавление контактов из CSV-файла.
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
    # Добавление контакта вручную.
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
    # Обновление данных контакта.
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
    # Просмотр контактов с фильтрами.
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
    # Удаление контакта по телефону или id.
    choice = input("Удалить по (1) телефону или (2) id? ")
    key = input("Введите значение: ").strip()
    with psycopg2.connect(**DataBase) as conn:
        with conn.cursor() as cur:
            if choice == '1':
                cur.execute("DELETE FROM phonebook WHERE phone = %s", (key,))
            else:
                cur.execute("DELETE FROM phonebook WHERE id = %s", (key,))
        conn.commit()
    print("Контакт удалён.")

# Меню
def main():
    init_db()
    while True:
        print("\nМеню Телефонной книги:")
        print("1. Импорт из CSV")
        print("2. Добавить контакт вручную")
        print("3. Обновить контакт")
        print("4. Поиск контактов")
        print("5. Удалить контакт")
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
        elif inp == '0':
            break

if __name__ == '__main__':
    main()