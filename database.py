import sqlite3

def init_db():
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            theta REAL,
            score REAL
        )
    """)
    conn.commit()
    conn.close()

def save_student(name, theta, score):
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO students (name, theta, score) VALUES (?, ?, ?)",
                (name, theta, score))
    conn.commit()
    conn.close()

def get_ranking():
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()
    cur.execute("SELECT name, score FROM students ORDER BY score DESC")
    data = cur.fetchall()
    conn.close()
    return data
