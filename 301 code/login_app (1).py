from PyQt5 import QtWidgets as qtw
from view import LoginView
from model import LoginManager
from controller import LoginController


if __name__ == "__main__":
    app = qtw.QApplication([])

    view = LoginView()
    model = LoginManager("credentials.db")
    controller = LoginController(model, view)


    view.show()
    app.exec_()
