from .varsWin import Ui_varsWin
from PyQt6.QtWidgets import QMainWindow


class VarWin(QMainWindow, Ui_varsWin):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Переменные и функции")
