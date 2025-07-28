import tkinter as tk
from tkinter import ttk
import sqlite3

# Создаём базу данных. Работаем сверху, после блока импорта.
def init_db():
    conn = sqlite3.connect('business_orders.db')
    cur = conn.cursor()
    cur.execute("""
CREATE TABLE IF NOT EXISTS orders (
id INTEGER PRIMARY KEY,
customer_name TEXT NOT NULL,
order_details TEXT NOT NULL,
status TEXT NOT NULL
)
""")
    conn.commit()
    conn.close()

# Функция для отображения заказов в таблице
def view_orders():
    for i in tree.get_children():
        tree.delete(i)

    conn = sqlite3.connect('business_orders.db')
    cur = conn.cursor()

    cur.execute("SELECT * FROM orders")
    rows = cur.fetchall()

    for row in rows:
        tree.insert("", tk.END, values=row)

    conn.close()

# Функция для добавления заказа
def add_order():
    conn = sqlite3.connect('business_orders.db')
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO orders (customer_name, order_details, status) VALUES (?, ?, 'Новый')",
        (customer_name_entry.get(), order_details_entry.get())
    )

    conn.commit()
    conn.close()

    # Очищаем поля ввода
    customer_name_entry.delete(0, tk.END)
    order_details_entry.delete(0, tk.END)

    # Обновляем таблицу
    view_orders()

def complete_order():
    selected_item = tree.selection()

    if selected_item:
        order_id = tree.item(selected_item, 'values')[0]

        conn = sqlite3.connect('business_orders.db')
        cur = conn.cursor()

        cur.execute("UPDATE orders SET status='Завершён' WHERE id=?", (order_id,))

        conn.commit()
        conn.close()

        view_orders()
    else:
        messagebox.showwarning("Предупреждение", "Выберите заказ для завершения")

# Создаём интерфейс
app = tk.Tk()
app.title("Система управления заказами")

# Инициализация базы данных
init_db()

# Надписи и поля для ввода
tk.Label(app, text="Имя клиента").pack()
customer_name_entry = tk.Entry(app)
customer_name_entry.pack()

tk.Label(app, text="Детали заказа").pack()
order_details_entry = tk.Entry(app)
order_details_entry.pack()

# Кнопка добавления заказа
add_button = tk.Button(app, text="Добавить заказ", command=add_order)
add_button.pack()

# Добавляем кнопку под предыдущей кнопкой:
complete_button = tk.Button(app, text="Завершить заказ", command=complete_order)
complete_button.pack()

# Создаем таблицу
columns = ("id", "customer_name", "order_details", "status")
tree = ttk.Treeview(app, columns=columns, show="headings")
for column in columns:
    tree.heading(column, text=column)
tree.pack()

# Загружаем текущие заказы
view_orders()

# Запуск Mainloop
app.mainloop()



