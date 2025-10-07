import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox, QLabel
)

class BookWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Manajemen Buku - Pelayanan Perpustakaan")
        self.setGeometry(200, 100, 900, 600)
        self.setup_ui()
        self.create_table()
        self.load_data()

    # -------------------- UI --------------------
    def setup_ui(self):
        layout = QVBoxLayout()

        # --- Input Fields ---
        form_layout = QHBoxLayout()
        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("ID Buku (boleh custom)")
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Judul Buku")
        self.author_input = QLineEdit()
        self.author_input.setPlaceholderText("Penulis")
        self.year_input = QLineEdit()
        self.year_input.setPlaceholderText("Tahun Terbit")

        form_layout.addWidget(self.id_input)
        form_layout.addWidget(self.title_input)
        form_layout.addWidget(self.author_input)
        form_layout.addWidget(self.year_input)

        # --- Buttons ---
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Tambah")
        self.edit_button = QPushButton("Edit")
        self.delete_button = QPushButton("Hapus")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Cari judul atau penulis...")
        self.search_button = QPushButton("Cari")

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.search_input)
        button_layout.addWidget(self.search_button)

        # --- Table View ---
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID Buku", "Judul", "Penulis", "Tahun"])
        self.table.setColumnWidth(0, 150)
        self.table.setColumnWidth(1, 350)
        self.table.setColumnWidth(2, 250)
        self.table.setColumnWidth(3, 100)

        # --- Add all to layout ---
        layout.addLayout(form_layout)
        layout.addLayout(button_layout)
        layout.addWidget(self.table)
        self.setLayout(layout)

        # --- Button actions ---
        self.add_button.clicked.connect(self.add_book)
        self.edit_button.clicked.connect(self.edit_book)
        self.delete_button.clicked.connect(self.delete_book)
        self.search_button.clicked.connect(self.search_books)

    # -------------------- DATABASE --------------------
    def connect_db(self):
        return sqlite3.connect("library.db")

    def create_table(self):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                year TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    def load_data(self):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books")
        rows = cursor.fetchall()
        conn.close()

        self.table.setRowCount(0)
        for row in rows:
            row_pos = self.table.rowCount()
            self.table.insertRow(row_pos)
            for col, data in enumerate(row):
                self.table.setItem(row_pos, col, QTableWidgetItem(str(data)))

    # -------------------- CRUD --------------------
    def add_book(self):
        id_buku = self.id_input.text().strip()
        title = self.title_input.text().strip()
        author = self.author_input.text().strip()
        year = self.year_input.text().strip()

        if not id_buku or not title or not author or not year:
            QMessageBox.warning(self, "Peringatan", "Semua kolom harus diisi!")
            return

        conn = self.connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO books (id, title, author, year) VALUES (?, ?, ?, ?)",
                           (id_buku, title, author, year))
            conn.commit()
            QMessageBox.information(self, "Sukses", "Buku berhasil ditambahkan!")
            self.load_data()
            self.clear_input()
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Error", "ID buku sudah ada, gunakan ID lain!")
        finally:
            conn.close()

    def edit_book(self):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Peringatan", "Pilih buku yang akan diedit!")
            return

        id_buku = self.table.item(selected_row, 0).text()
        title = self.title_input.text().strip()
        author = self.author_input.text().strip()
        year = self.year_input.text().strip()

        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE books SET title=?, author=?, year=? WHERE id=?",
                       (title, author, year, id_buku))
        conn.commit()
        conn.close()
        QMessageBox.information(self, "Sukses", "Data buku berhasil diperbarui!")
        self.load_data()

    def delete_book(self):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Peringatan", "Pilih buku yang akan dihapus!")
            return

        id_buku = self.table.item(selected_row, 0).text()
        confirm = QMessageBox.question(
            self, "Konfirmasi", f"Hapus buku dengan ID {id_buku}?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM books WHERE id=?", (id_buku,))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Sukses", "Buku berhasil dihapus!")
            self.load_data()

    def search_books(self):
        keyword = self.search_input.text().strip()
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM books
            WHERE title LIKE ? OR author LIKE ?
        """, (f"%{keyword}%", f"%{keyword}%"))
        rows = cursor.fetchall()
        conn.close()

        self.table.setRowCount(0)
        for row in rows:
            row_pos = self.table.rowCount()
            self.table.insertRow(row_pos)
            for col, data in enumerate(row):
                self.table.setItem(row_pos, col, QTableWidgetItem(str(data)))

    def clear_input(self):
        self.id_input.clear()
        self.title_input.clear()
        self.author_input.clear()
        self.year_input.clear()
        self.search_input.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BookWindow()
    window.show()
    sys.exit(app.exec_())
