import sqlite3

def init_db():
    conn = sqlite3.connect("raf_store.db")
    cursor = conn.cursor()
    
    # Таблица товаров
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    """)
    
    # Таблица клиентов / программы лояльности
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS loyalty_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            points INTEGER DEFAULT 0
        )
    """)
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully!")
