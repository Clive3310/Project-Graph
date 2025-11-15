from .mainWin import Ui_windowMain
from PyQt6.QtWidgets import QMainWindow


class MainWin(QMainWindow, Ui_windowMain):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Graphic Calculator")
        self.tabWidget.setTabText(0, "📈 Plotting")
        self.tabWidget.setTabText(1, "💾 Saving")