import sqlite3


class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, item text, product type text, store text, price text)")
        self.conn.commit()

    def fetch(self):
        self.cur.execute("SELECT * FROM items")
        rows = self.cur.fetchall()
        return rows

    def insert(self, item, product_type, store, price):
        self.cur.execute("INSERT INTO parts VALUES (NULL, ?, ?, ?, ?)",
                         (item, product_type, store, price))
        self.conn.commit()

    def remove(self, id):
        self.cur.execute("DELETE FROM items WHERE id=?", (id,))
        self.conn.commit()

    def update(self, id, item, product_type, store, price):
        self.cur.execute("UPDATE items SET item = ?, product type = ?, store = ?, price = ? WHERE id = ?",
                         (item, product_type, store, price, id))
        self.conn.commit()

    def __del__(self):
        self.conn.close()
