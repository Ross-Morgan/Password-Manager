# Module imports
from PyQt5 import QtGui, QtWidgets
from enum import auto, Enum

import sys
import re

# File imports
from mainwindow import MainWindow
from database import user_db, User, UserData

WIDTH, HEIGHT = 320, 200

class Modes(Enum):
    LOGIN = auto()
    SIGNUP = auto()


class LoginWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(LoginWindow, self).__init__(parent)

        self.mode = Modes.LOGIN

        self.font_ = QtGui.QFont("Helvetica", 18)

        self.setup_ui()
        self.setup_shortcuts()

    def setup_shortcuts(self):
        self.login_shortcut = QtWidgets.QShortcut(self, key=QtGui.QKeySequence("enter"))
        self.login_shortcut.activated.connect(self.on_submit)

    def setup_ui(self):
        self.setFixedSize(WIDTH, HEIGHT)
        self.setWindowTitle("Login to Password Manager")
        self.setWindowIcon(QtGui.QIcon("Assets/enter.png"))

        self.username_field = QtWidgets.QLineEdit(self, placeholderText="Username")
        self.password_field = QtWidgets.QLineEdit(self, placeholderText="Password")

        self.username_field.setGeometry(10, 10, 300, 56)
        self.password_field.setGeometry(10, 70, 300, 56)

        self.username_field.setFont(self.font_)
        self.password_field.setFont(self.font_)

        self.password_field.setEchoMode(QtWidgets.QLineEdit.Password)

        self.submit_button = QtWidgets.QPushButton(self, text="Login")
        self.submit_button.setGeometry(10, 130, 100, 56)
        self.submit_button.setFont(self.font_)
        self.submit_button.clicked.connect(self.on_submit)

        self.account_button = QtWidgets.QPushButton(self, text="I don't have an account")
        self.account_button.setGeometry(120, 130, 190, 56)
        self.account_button.setFont(QtGui.QFont("Helvetica", 12, 5))
        self.account_button.clicked.connect(self.on_account)

    def on_account(self):
        if self.mode == Modes.LOGIN:
            self.mode = Modes.SIGNUP
            self.submit_button.setText("Sign Up")
            self.account_button.setText("I already have an account")
        else:
            self.mode = Modes.LOGIN
            self.submit_button.setText("Login")
            self.account_button.setText("I don't have an account")

    def on_submit(self):
        submitted_username = self.username_field.text()
        submitted_password = self.password_field.text()

        if not re.search(r"^[\w\-. ]+$", submitted_username):
            QtWidgets.QMessageBox.question(self, "Error", "Illegal Username", QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
            return


        if self.mode == Modes.LOGIN:
            user_db.cur.execute("select password from Users where name=?", (submitted_username,))

            query_result = user_db.cur.fetchone()

            if query_result is None:
                query_result = (None,)

            if query_result[0] == submitted_password:
                self.on_success()
            else:
                QtWidgets.QMessageBox.question(self, "Error", "Incorrect Username or Password", QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
                self.password_field.setText("")

        else: # self.mode == Modes.SIGNUP

            user_db.cur.execute("insert into Users(name,password) values(?,?)", (submitted_username, submitted_password))
            user_db.con.commit()

            QtWidgets.QMessageBox.question(self, "Created User", "Successfully created account", QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)

            self.username_field.setText("")
            self.password_field.setText("")

    def on_success(self):
        user_db.con.commit()

        self.main_window = MainWindow(self.username_field.text())

        self.hide()
        self.main_window.show()


def main():
    app = QtWidgets.QApplication(sys.argv)

    window = LoginWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
