from .regWin import Ui_regWin
from PyQt6.QtWidgets import QMainWindow


class RegWin(QMainWindow, Ui_regWin):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Registration")
        self.errorLabel.setText("")
