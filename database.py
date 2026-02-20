import sqlite3

def init_db():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        category TEXT,
        amount REAL,
        notes TEXT
    )''')
    conn.commit()
    conn.close()

def insert_expense(date, category, amount, notes):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("INSERT INTO expenses (date, category, amount, notes) VALUES (?, ?, ?, ?)",
              (date, category, amount, notes))
    conn.commit()
    conn.close()

def get_all_expenses():
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("SELECT * FROM expenses ORDER BY date DESC")
    data = c.fetchall()
    conn.close()
    return data

def delete_expense(expense_id):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()

def update_expense_by_id(expense_id, date, category, amount, notes):
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    c.execute("""
        UPDATE expenses 
        SET date = ?, category = ?, amount = ?, notes = ?
        WHERE id = ?
    """, (date, category, amount, notes, expense_id))
    conn.commit()
    conn.close()