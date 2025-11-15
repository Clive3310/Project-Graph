import sys
from PyQt6.QtWidgets import QApplication
from controller import Controller


def main(argv):
    app = QApplication(argv)
    cont = Controller()
    cont.startMain()
    sys.exit(app.exec())


if __name__ == "__main__":
    main(sys.argv)
