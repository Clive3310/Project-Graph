from .createVarForm import Ui_createVarForm
from PyQt6.QtWidgets import QMainWindow


class VarForm(QMainWindow, Ui_createVarForm):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Создание переменой")
        self.errorLabel.setText("")
