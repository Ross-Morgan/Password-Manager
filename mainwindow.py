# Module imports
from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3
import sys

# File imports
from database import Database

WIDTH, HEIGHT = 640, 480

class MainWindow(QtWidgets.QMainWindow):
    user: str
    """Main Window class for the application"""
    def __init__(self, user: str, parent=None):
        # Initialise parent class
        super(MainWindow, self).__init__(parent)

        self.font_ = QtGui.QFont("Helvetica", 18)

        self.db = Database()
        self.db.con = sqlite3.connect(f"Databases/{user}.db")
        self.db.cur = self.db.con.cursor()
        self.db.cur.execute("""
            create table if not exists Passwords (account text not null primary key, password text);
        """)
        self.db.con.commit()

        self.init_ui()

    def init_ui(self):
        self.setFixedSize(WIDTH, HEIGHT)

        self.table_widget = QtWidgets.QTableWidget(self)
        self.table_widget.setGeometry(10, 10, 252, 460)
        self.table_widget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.table_widget.setMaximumWidth(300)
        self.table_widget.setColumnCount(2)
        self.table_widget.setColumnWidth(0, 100)
        self.table_widget.setColumnWidth(1, 150)
        self.table_widget.setHorizontalHeaderLabels(["Account", "Password"])

        self.account_field = QtWidgets.QLineEdit(self, placeholderText="Account:")
        self.account_field.setGeometry(380, 10, 250, 56)
        self.account_field.setFont(self.font_)

        self.password_field = QtWidgets.QLineEdit(self, placeholderText="Password:")
        self.password_field.setGeometry(380, 70, 250, 56)
        self.password_field.setFont(self.font_)

        self.add_field_button = QtWidgets.QPushButton(self, text="Add Field")
        self.add_field_button.setGeometry(510, 130, 120, 56)
        self.add_field_button.setFont(self.font_)
        self.add_field_button.clicked.connect(self.add_field)


        self.remove_account_field = QtWidgets.QLineEdit(self, placeholderText="Account:")
        self.remove_account_field.setGeometry(380, 240, 250, 56)
        self.remove_account_field.setFont(self.font_)

        self.remove_field_button = QtWidgets.QPushButton(self, text="Remove Field")
        self.remove_field_button.setGeometry(470, 300, 160, 56)
        self.remove_field_button.setFont(self.font_)
        self.remove_field_button.clicked.connect(self.remove_field)


        self.load_sqlite_data()

    def load_sqlite_data(self):
        self.db.cur.execute("select * from Passwords")

        data = self.db.cur.fetchall()

        self.table_widget.setRowCount(len(data))



        for table_row, row in enumerate(data):
            self.table_widget.setItem(table_row, 0, QtWidgets.QTableWidgetItem(row[0]))
            self.table_widget.setItem(table_row, 1, QtWidgets.QTableWidgetItem(row[1]))

    def add_field(self):
        account = self.account_field.text()
        password = self.password_field.text()

        try:
            self.db.cur.execute("insert into Passwords(account, password) values (?,?)", (account, password))
        except sqlite3.IntegrityError:
            QtWidgets.QMessageBox.question(self, "Error", f"Entry with name {account} already exists", QtWidgets.QMessageBox.Ok, QtWidgets.MessageBox.Ok)
        finally:
            self.db.con.commit()

        self.load_sqlite_data()

    def remove_field(self):
        account = self.remove_account_field.text()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow("Ross Morgan")
    window.show()

    sys.exit(app.exec())
