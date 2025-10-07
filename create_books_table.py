import sqlite3

# Koneksi ke database utama
conn = sqlite3.connect("library.db")
cursor = conn.cursor()

# Membuat tabel 'books' jika belum ada
cursor.execute('''
CREATE TABLE IF NOT EXISTS books (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    year TEXT NOT NULL
)
''')

conn.commit()
conn.close()

print("✅ Tabel 'books' berhasil dibuat di library.db!")
