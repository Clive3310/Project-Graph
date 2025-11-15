from .mainWin import Ui_windowMain
from PyQt6.QtWidgets import QMainWindow


class MainWin(QMainWindow, Ui_windowMain):
    def __init__(self):
        super().__init__()
        self.setupUi(self)