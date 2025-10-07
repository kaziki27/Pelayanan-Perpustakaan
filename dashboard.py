from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QMessageBox, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt
from qt_material import apply_stylesheet
import sys


class DashboardWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📚 Dashboard Pelayanan Perpustakaan")
        
        # Ukuran window diperbesar
        self.showMaximized()  # X, Y, Lebar, Tinggi
        self.initUI()

    def initUI(self):
        # Widget dan layout utama
        central_widget = QWidget()
        layout = QVBoxLayout()

        # Label judul besar
        label = QLabel("Selamat Datang di Dashboard Perpustakaan Digital")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("""
            font-size: 26px;
            font-weight: bold;
            color: #2E86C1;
            margin-top: 40px;
        """)
        layout.addWidget(label)

        # Spasi kosong untuk mempercantik tata letak
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Tombol menu besar
        self.btn_books = QPushButton("📘 Manajemen Buku")
        self.btn_members = QPushButton("👥 Data Peminjam")
        self.btn_logout = QPushButton("🚪 Logout")

        for btn in [self.btn_books, self.btn_members, self.btn_logout]:
            btn.setFixedHeight(60)
            btn.setStyleSheet("""
                font-size: 18px;
                font-weight: 600;
                border-radius: 12px;
                margin: 10px 100px;
            """)
            layout.addWidget(btn)

        # Spasi bawah agar tombol tidak terlalu menempel ke tepi
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Event tombol
        self.btn_books.clicked.connect(self.open_books)
        self.btn_members.clicked.connect(self.open_members)
        self.btn_logout.clicked.connect(self.logout)

        # Set layout
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def open_books(self):
        self.close()
        import books
        self.books_window = books.BooksWindow()
        self.books_window.show()

        QMessageBox.information(self, "Info", "📚 Fitur Manajemen Buku belum diimplementasikan.")

    def open_members(self):
        QMessageBox.information(self, "Info", "👥 Fitur Data Peminjam belum diimplementasikan.")

    def logout(self):
        reply = QMessageBox.question(
            self, "Konfirmasi Logout", "Apakah Anda yakin ingin logout?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.close()
            import login
            self.login_window = login.LoginWindow()
            self.login_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='dark_blue.xml')
    window = DashboardWindow()
    window.show()
    sys.exit(app.exec_())
