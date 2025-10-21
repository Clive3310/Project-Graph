from PyQt6.QtCore import QPointF
from PyQt6.QtWidgets import QApplication, QMainWindow
import sys
from PyQt6.QtGui import QColor, QPainter, QPixmap
from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_windowMain(object):
    def setupUi(self, windowMain):
        windowMain.setObjectName("windowMain")
        windowMain.resize(900, 520)
        self.btnPlot = QtWidgets.QPushButton(parent=windowMain)
        self.btnPlot.setGeometry(QtCore.QRect(10, 60, 370, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btnPlot.setFont(font)
        self.btnPlot.setObjectName("btnPlot")
        self.btnClear = QtWidgets.QPushButton(parent=windowMain)
        self.btnClear.setGeometry(QtCore.QRect(10, 110, 370, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btnClear.setFont(font)
        self.btnClear.setObjectName("btnClear")
        self.funcList = QtWidgets.QListWidget(parent=windowMain)
        self.funcList.setGeometry(QtCore.QRect(10, 159, 370, 350))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.funcList.setFont(font)
        self.funcList.setObjectName("funcList")
        self.funcEdit = QtWidgets.QLineEdit(parent=windowMain)
        self.funcEdit.setGeometry(QtCore.QRect(60, 10, 320, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.funcEdit.setFont(font)
        self.funcEdit.setObjectName("funcEdit")
        self.yInd = QtWidgets.QLabel(parent=windowMain)
        self.yInd.setGeometry(QtCore.QRect(20, 10, 60, 40))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.yInd.setFont(font)
        self.yInd.setObjectName("yInd")
        self.canvasL = QtWidgets.QLabel(parent=windowMain)
        self.canvasL.setGeometry(QtCore.QRect(390, 10, 500, 500))
        self.canvasL.setText("")
        self.canvasL.setObjectName("canvasL")

        self.retranslateUi(windowMain)
        self.funcList.setCurrentRow(-1)
        QtCore.QMetaObject.connectSlotsByName(windowMain)

    def retranslateUi(self, windowMain):
        _translate = QtCore.QCoreApplication.translate
        windowMain.setWindowTitle(_translate("windowMain", "Form"))
        self.btnPlot.setText(_translate("windowMain", "Построить"))
        self.btnClear.setText(_translate("windowMain", "Очистить"))
        self.funcList.setSortingEnabled(False)
        self.yInd.setText(_translate("windowMain", "y ="))


def getCoords(func, rng, exp) -> list[tuple[float, float] | None]:
    coords = []
    if "^" in func:
        func = func.replace("^", "**")
    for x in rng:
        x = round(x / exp, 5)
        y = 0
        try:
            y = round(eval(func), 5)
        except Exception as e:
            print(f"Function '{func}' dropped with: {x, y}")
            print(f"---- {e}\n")
            coords.append(None)
            continue
        coords.append((float(x), float(y)))
    return coords


class MainWindow(QMainWindow, Ui_windowMain):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setup()

    def setup(self):
        self.clearCanvas()
        self.setupBack()
        self.plotFunc("x^2")

    def setupBack(self):
        self.btnPlot.clicked.connect(self.plotFunc)
        self.btnClear.clicked.connect(self.clearCanvas)

    def plotFunc(self, func):
        for p in getCoords(func, range(-250, 251), 1):
            if p is None:
                continue
            self.drawPoint(self.refCoords(p))
        print("Ended drawing func:", func)

    def clearCanvas(self):
        canvas = QPixmap(500, 500)
        canvas.fill(QColor('white'))
        self.canvasL.setPixmap(canvas)

    def drawPoint(self, coords: tuple[float, float]):
        canvas = self.canvasL.pixmap()
        painter = QPainter(canvas)
        painter.drawPoint(QPointF(*coords))
        painter.end()
        self.canvasL.setPixmap(canvas)

    def refCoords(self, coords):
        coords = (self.canvasL.width() // 2 + coords[0], self.canvasL.height() // 2 - coords[1])
        return coords


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
