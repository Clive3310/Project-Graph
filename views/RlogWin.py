from .logWin import Ui_logWin
from PyQt6.QtWidgets import QMainWindow


class LogWin(QMainWindow, Ui_logWin):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Logging")
        self.errorLabel.setText("")
