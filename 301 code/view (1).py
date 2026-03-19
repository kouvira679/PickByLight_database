from PyQt5 import uic # To load a ui file
from PyQt5 import QtWidgets as qtw # Create Qt Widgets
from PyQt5.QtCore import pyqtSignal

class LoginView(qtw.QWidget):
    # Define the signals
    login_requested = pyqtSignal(str, str) # Comes with username and password
    register_requested = pyqtSignal(str, str)
    update_pwd = pyqtSignal(str, str, str)

    def __init__(self):
        super().__init__()

        # Load the ui file
        uic.loadUi("login_window.ui", self)

        # Register the login button callback function
        self.login_btn.clicked.connect(self.check_credentials)

        self.register_btn.clicked.connect(self.add_new_user)

        self.update_btn.clicked.coonect(self.update_password)

    def check_credentials(self):
        username = self.username.text()
        password = self.password.text()
        self.login_requested.emit(username, password)

    # Create methods to pop-up a message to the user to be called by the controller
    def show_success(self, message):
        qtw.QMessageBox.information(self, "Success", message)

    def show_failed(self, message):
        qtw.QMessageBox.information(self, "Fail", message)

    def add_new_user(self):
        username = self.username.text()
        password = self.password.text()
        self.register_requested.emit(username, password)

    def update_password(self):
        username = self.username.text()
        password = self.password.text()
        new_password = self.new_pwd.text()
        self.update_pwd.emit(username, password, new_password)
