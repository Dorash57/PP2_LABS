import psycopg2 
import tkinter as tk
from tkinter import messagebox, ttk

# Подключение к базе данных
conn = psycopg2.connect(
    host="localhost",
    dbname="lab10",
    user="postgres",
    password="Ilyas7002zxz",
    port=5432
)
cur = conn.cursor()

# Создание таблицы
cur.execute("""
    CREATE TABLE IF NOT EXISTS phonebook (
        user_id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        surname VARCHAR(255) NOT NULL,
        phone VARCHAR(255) NOT NULL
    )
""")
conn.commit()

# Функции

def insert_data():
    name = entry_name.get()
    surname = entry_surname.get()
    phone = entry_phone.get()

    if not (name and surname and phone):
        messagebox.showwarning("Input Error", "Please fill all fields")
        return

    if not phone.isdigit() or len(phone) != 11:
        messagebox.showerror("Phone Error", "Phone must be 11 digits and contain only numbers.")
        return

    cur.execute("INSERT INTO phonebook (name, surname, phone) VALUES (%s, %s, %s)", (name, surname, phone))
    conn.commit()
    messagebox.showinfo("Success", "Contact added")
    refresh_table()

def delete_data():
    phone = entry_phone.get()
    cur.execute("DELETE FROM phonebook WHERE phone = %s", (phone,))
    conn.commit()
    messagebox.showinfo("Deleted", "Contact deleted (if existed)")
    refresh_table()

def update_data():
    phone = entry_phone.get()
    new_name = entry_name.get()
    new_surname = entry_surname.get()
    cur.execute("UPDATE phonebook SET name = %s, surname = %s WHERE phone = %s", (new_name, new_surname, phone))
    conn.commit()
    messagebox.showinfo("Updated", "Contact updated")
    refresh_table()

def refresh_table():
    for row in tree.get_children():
        tree.delete(row)
    cur.execute("SELECT * FROM phonebook")
    rows = cur.fetchall()
    for row in rows:
        tree.insert("", tk.END, values=row)

def search_by_phone():
    phone = entry_search.get()
    for row in tree.get_children():
        tree.delete(row)
    cur.execute("SELECT * FROM phonebook WHERE phone = %s", (phone,))
    rows = cur.fetchall()
    for row in rows:
        tree.insert("", tk.END, values=row)

# UI
root = tk.Tk()
root.title("PhoneBook GUI")
root.geometry("600x500")

frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Name").grid(row=0, column=0)
entry_name = tk.Entry(frame)
entry_name.grid(row=0, column=1)

tk.Label(frame, text="Surname").grid(row=1, column=0)
entry_surname = tk.Entry(frame)
entry_surname.grid(row=1, column=1)

tk.Label(frame, text="Phone").grid(row=2, column=0)
entry_phone = tk.Entry(frame)
entry_phone.grid(row=2, column=1)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Add", command=insert_data).grid(row=0, column=0, padx=10)
tk.Button(btn_frame, text="Update", command=update_data).grid(row=0, column=1, padx=10)
tk.Button(btn_frame, text="Delete", command=delete_data).grid(row=0, column=2, padx=10)
tk.Button(btn_frame, text="Refresh", command=refresh_table).grid(row=0, column=3, padx=10)

# Поиск
search_frame = tk.Frame(root)
search_frame.pack(pady=10)

tk.Label(search_frame, text="Search by Phone").grid(row=0, column=0)
entry_search = tk.Entry(search_frame)
entry_search.grid(row=0, column=1)
tk.Button(search_frame, text="Search", command=search_by_phone).grid(row=0, column=2, padx=10)

# Таблица
cols = ("ID", "Name", "Surname", "Phone")
tree = ttk.Treeview(root, columns=cols, show="headings")
for col in cols:
    tree.heading(col, text=col)
    tree.column(col, width=100)
tree.pack(expand=True, fill='both')

refresh_table()
root.mainloop()

cur.close()
conn.close()