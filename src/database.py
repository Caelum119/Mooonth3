import sqlite3

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cur = self.conn.cursor()

    def create_table(self):
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount INTEGER NOT NULL,
                category TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def add_expense(self, amount, category):
        self.cur.execute("INSERT INTO expenses (amount, category) VALUES (?, ?)", (amount, category))
        self.conn.commit()

    def all_expenses(self):
        self.cur.execute("SELECT * FROM expenses")
        return self.cur.fetchall()

    def delete_expense(self, expense_id):
        self.cur.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        self.conn.commit()

    def update_expense(self, expense_id, amount, category):
        self.cur.execute("UPDATE expenses SET amount=?, category=? WHERE id=?", (amount, category, expense_id))
        self.conn.commit()

    def get_expense(self, expense_id):
        self.cur.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,))
        return self.cur.fetchone()

    def total_sum(self):
        self.cur.execute("SELECT SUM(amount) FROM expenses")
        total = self.cur.fetchone()[0]
        return total if total else 0
