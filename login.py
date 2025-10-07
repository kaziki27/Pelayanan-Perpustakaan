from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QMessageBox, QVBoxLayout
)
from qt_material import apply_stylesheet  # untuk tema qt_material
import sys
import sqlite3


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login Resepsionis - Perpustakaan")
        self.setGeometry(600, 300, 420, 300)

        self.initUI()
        self.create_db()

    # =========================
    # Membuat tampilan login UI
    # =========================
    def initUI(self):
        layout = QVBoxLayout()

        # Logo
        self.logo_label = QLabel()
        pixmap = QPixmap("logo.png")
        pixmap = pixmap.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.logo_label.setPixmap(pixmap)
        self.logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.logo_label)

        # Input Username
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Masukkan Username")
        layout.addWidget(self.username_input)

        # Input Password
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Masukkan Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        # Tombol Login
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.check_login)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    # =========================
    # Membuat database jika belum ada
    # =========================
    def create_db(self):
        conn = sqlite3.connect("database/resepsionis.db")
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS resepsionis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()

        # Tambahkan akun default jika belum ada
        cursor.execute("SELECT * FROM resepsionis WHERE username=?", ("admin",))
        if not cursor.fetchone():
            cursor.execute("INSERT INTO resepsionis (username, password) VALUES (?, ?)", ("admin", "12345"))
            conn.commit()
        conn.close()

    # =========================
    # Mengecek login user
    # =========================
    def check_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        conn = sqlite3.connect("database/resepsionis.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM resepsionis WHERE username=? AND password=?", (username, password))
        result = cursor.fetchone()
        conn.close()

        if result:
            QMessageBox.information(self, "Sukses", "Login Berhasil!")
            self.close()
            import dashboard
            self.dashboard = dashboard.DashboardWindow()
            self.dashboard.show()
        else:
            QMessageBox.warning(self, "Error", "Username atau Password salah!")


# =========================
# Program Utama
# =========================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='dark_blue.xml')  # tema qt_material
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
