from PyQt6.QtCore import QPointF
from PyQt6.QtWidgets import QApplication, QMainWindow
import sys
from random import choice
from math import sin, cos, pi
from PyQt6.QtGui import QColor, QPainter, QPixmap, QPen, QIcon
from Ui_file import Ui_WindowMain


def getCoords(func: str, rng: range, exp: int) -> tuple[list[tuple[float, float] | None], bool]:
    coords = []
    good = False
    if "^" in func:
        func = func.replace("^", "**")
    for x in rng:
        x = round(x / exp, 5)
        y = 0.0
        try:
            y = round(eval(func), 3)
        except Exception as e:
            print(f"Function '{func}' dropped with: {x, y}")
            print(f"---- {e}\n")
            coords.append(None)
            continue
        coords.append((float(x), float(y)))
        good = True
    return coords, good


class MainWindow(QMainWindow, Ui_WindowMain):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setup()

    def setup(self):
        self.setFixedSize(900, 520)
        self.setWindowIcon(QIcon("./res/icon.png"))

        self.funcBank = dict()
        self.colorBank = [QColor('red'), QColor('black'), QColor('blue'),
                          QColor('green'), QColor('purple'), QColor('magenta')]
        self.funcColorLook = self.colorBank.copy()
        self.pointWidth = 2
        self.painter = QPainter()
        self.painter.setRenderHint(QPainter.RenderHint.Antialiasing)  # Вроде с этим чуть ровнее
        self.pen = QPen()
        self.pen.setWidth(self.pointWidth)
        self.clear()
        self.setupBack()
        # self.plotFunc("x^2+2*x-1")
        # self.plotFunc("x + 3")

    def setupBack(self):
        self.btnPlot.clicked.connect(self.plotButt)
        self.btnClear.clicked.connect(self.clear)

    def plotButt(self):
        func = self.funcEdit.text().strip()
        if func and func not in self.funcBank.keys():
            coords = self.plotFunc(func)
            if coords is None:
                self.funcEdit.setText("Function failed!")
                return
            self.funcBank[func] = coords
            if self.funcList.item(0).text() == "Empty!":
                self.funcList.clear()
            self.funcList.addItem("y = " + func)

    def plotFunc(self, func: str) -> list[tuple[float, float] | None] | None:
        # for p in getCoords(func, range(-250, 251), 10):
        #     self.drawPoint(self.refCoords(p))
        coords, flag = getCoords(func, range(-12500, 12501), 1000)
        if not flag:
            return None

        output = []
        temp = []
        for item in coords:  # Разделение функции на 'регионы'
            if item is None:
                output.append(temp)
                temp = []
            else:
                temp.append(item)
        if temp:
            output.append(temp)

        canvas = self.canvasL.pixmap()
        self.painter.begin(canvas)
        if len(self.funcBank.keys()) < 6:  # Выбор цвета функции
            color = choice(self.funcColorLook)
            self.funcColorLook.remove(color)
        else:
            color = choice(self.colorBank)
        self.pen.setColor(color)
        self.painter.setPen(self.pen)

        for p_list in output:
            self.painter.drawLines(list(map(lambda p: QPointF(*self.refCoords(p)), p_list)))
        self.painter.end()
        self.canvasL.setPixmap(canvas)
        print("Ended drawing func:", func)
        return coords.copy()

    def clear(self):
        canvas = QPixmap(500, 500)
        canvas.fill(QColor('white'))
        self.canvasL.setPixmap(canvas)
        self.funcList.clear()
        self.funcList.addItem("Empty!")
        self.funcBank.clear()
        self.funcColorLook = self.colorBank.copy()
        self.funcEdit.clear()

    def drawPoint(self, coords: tuple[float, float]):
        canvas = self.canvasL.pixmap()
        self.painter.begin(canvas)
        self.painter.setPen(self.pen)
        self.painter.drawPoint(QPointF(*coords))
        self.painter.end()
        self.canvasL.setPixmap(canvas)

    def refCoords(self, coords: tuple[float, float]) -> tuple[float, float]:
        coords = (self.canvasL.width() // 2 + coords[0] * 20, self.canvasL.height() // 2 - coords[1] * 20)
        return coords


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
