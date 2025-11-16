from .proWin import Ui_proWin
from PyQt6.QtWidgets import QMainWindow


class ProWin(QMainWindow, Ui_proWin):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Профиль")
