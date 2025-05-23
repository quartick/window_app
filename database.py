import sqlite3

# Создаем базу данных и таблицу
def create_database():
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()

    # Создаем таблицу заказов с типом стеклопакета
    cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        width INTEGER NOT NULL,
                        height INTEGER NOT NULL,
                        package_type TEXT NOT NULL)''')

    # Создание таблицы производственных заказов
    cursor.execute("""
           CREATE TABLE IF NOT EXISTS production_orders (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               name TEXT NOT NULL,
               customer TEXT,
               deadline DATE NOT NULL,
               priority TEXT NOT NULL,
               status TEXT NOT NULL
           )
       """)

    # Создание таблицы стеклопакетов в производственных заказах
    cursor.execute("""
           CREATE TABLE IF NOT EXISTS production_order_windows (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               order_id INTEGER NOT NULL,
               type TEXT NOT NULL,
               width INTEGER NOT NULL,
               height INTEGER NOT NULL,
               quantity INTEGER NOT NULL,
               FOREIGN KEY(order_id) REFERENCES production_orders(id)
           )
       """)

    # Создание таблицы материалов для производственных заказов
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS production_order_materials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL,
                type TEXT NOT NULL,
                amount REAL NOT NULL,
                dimension TEXT NOT NULL,
                FOREIGN KEY(order_id) REFERENCES production_orders(id)
            )
        """)

    conn.commit()
    conn.close()

def add_order_to_db(package_type, width, height, quantity):
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()

    # Вставляем заказ с указанием типа стеклопакета
    cursor.execute("INSERT INTO orders (package_type, width, height, quantity) VALUES (?, ?, ?, ?)",
                   (package_type, width, height, quantity))
    conn.commit()
    conn.close()

def delete_order_from_db(order_id):
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM orders WHERE id = ?", (order_id,))
    conn.commit()
    conn.close()

def update_order_in_db(order_id, new_width, new_height):
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE orders SET width = ?, height = ? WHERE id = ?", (new_width, new_height, order_id))
    conn.commit()
    conn.close()

def get_all_orders_from_db():
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()

    # Добавляем выбор типа стеклопакета
    cursor.execute("SELECT id, width, height, package_type FROM orders")
    orders = cursor.fetchall()
    conn.close()
    return orders


def add_production_order(name, customer, deadline, priority, status):
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()
    cursor.execute("""
            INSERT INTO production_orders (name, customer, deadline, priority, status)
            VALUES (?, ?, ?, ?, ?)
        """, (name, customer, deadline, priority, status))
    conn.commit()
    conn.close()
    return cursor.lastrowid  # <- Это критически важно!




def get_production_orders():
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM production_orders ORDER BY deadline")
    orders = cursor.fetchall()
    conn.close()
    return orders

def update_production_order_status(order_id, new_status):
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE production_orders 
        SET status = ?
        WHERE id = ?
    """, (new_status, order_id))
    conn.commit()
    conn.close()

def delete_production_order(order_id):
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM production_orders WHERE id = ?", (order_id,))
    conn.commit()
    conn.close()

def add_window_to_production_order(order_id, window_type, width, height, quantity):
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO production_order_windows (order_id, type, width, height, quantity)
        VALUES (?, ?, ?, ?, ?)
    """, (order_id, window_type, width, height, quantity))
    conn.commit()
    conn.close()

def get_windows_for_production_order(order_id):
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, type, width, height, quantity 
        FROM production_order_windows 
        WHERE order_id = ?
        ORDER BY id
    """, (order_id,))
    windows = cursor.fetchall()
    conn.close()
    return windows

def delete_window_from_production_order(window_id):
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM production_order_windows WHERE id = ?", (window_id,))
    conn.commit()
    conn.close()

def add_material_to_production_order(order_id, material_type, amount, dimension):
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO production_order_materials (order_id, type, amount, dimension)
        VALUES (?, ?, ?, ?)
    """, (order_id, material_type, amount, dimension))
    conn.commit()
    conn.close()

def get_materials_for_production_order(order_id):
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, type, amount, dimension 
        FROM production_order_materials 
        WHERE order_id = ?
        ORDER BY id
    """, (order_id,))
    materials = cursor.fetchall()
    conn.close()
    return materials

def delete_material_from_production_order(material_id):
    conn = sqlite3.connect('orders.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM production_order_materials WHERE id = ?", (material_id,))
    conn.commit()
    conn.close()