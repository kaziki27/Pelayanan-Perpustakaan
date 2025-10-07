import sqlite3

# Membuat / membuka database
conn = sqlite3.connect("library.db")
cursor = conn.cursor()

# Membuat tabel users jika belum ada
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
""")

# Tambahkan akun default (admin)
cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", ("admin", "123"))

conn.commit()
conn.close()

print("Database dan tabel users berhasil dibuat!")
