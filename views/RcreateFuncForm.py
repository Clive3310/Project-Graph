from .createFuncForm import Ui_createFuncForm
from PyQt6.QtWidgets import QMainWindow


class FuncForm(QMainWindow, Ui_createFuncForm):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Создание функции")
        self.errorLabel.setText("")
