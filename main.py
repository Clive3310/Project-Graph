from PyQt6.QtCore import QPointF
from PyQt6.QtWidgets import QApplication, QMainWindow
import sys
from random import choice
from math import sin, cos, pi
from PyQt6.QtGui import QColor, QPainter, QPixmap, QPen, QIcon
from Ui_file import Ui_WindowMain

WIN_SIZE = 900, 520
CANVAS_SIZE = 500, 500
# RANGE_BORDERS = -12500, 12501 - Реальная граница
RANGE_BORDERS = -12450, 12450
EXP = 1000
COLOR_BANK = [QColor('red'), QColor('blue'), QColor('green'), QColor('purple'), QColor('magenta')]
POINT_DIF = 20


def getCoords(func: str, rng: range, exp: int) -> tuple[list[tuple[float, float] | None], dict[str, bool]]:
    coords = []
    log = {"hasPoints": False, "hasPointsInRange": False}
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
        if 0 <= CANVAS_SIZE[1] // 2 - y * POINT_DIF <= CANVAS_SIZE[1]:
            log["hasPointsInRange"] = True
        coords.append((float(x), float(y)))
        log["hasPoints"] = True
    return coords, log


class MainWindow(QMainWindow, Ui_WindowMain):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setup()

    def setup(self):
        self.setFixedSize(*WIN_SIZE)
        self.setWindowIcon(QIcon("./res/icon.png"))
        self.XFuncData = getCoords("0", range(*RANGE_BORDERS), EXP)[0]
        self.funcBank = dict()  # {funcName: (coords, color)}
        self.colorBank = COLOR_BANK.copy()
        self.funcColorLook = self.colorBank.copy()
        self.pointWidth = 2
        self.painter = QPainter()
        self.painter.setRenderHint(QPainter.RenderHint.Antialiasing)  # Вроде с этим чуть ровнее
        self.pen = QPen()
        self.pen.setWidth(self.pointWidth)
        self.clear()
        self.setupBack()

    def setupBack(self):
        self.btnPlot.clicked.connect(self.plotButt)
        self.btnClear.clicked.connect(self.clear)

    def plotButt(self):
        func = self.funcEdit.text().strip()
        if (func and func not in self.funcBank.keys() and
                func != "Function failed!" and func != "Function failed! Out of range!"):
            coords, log = getCoords(func, range(*RANGE_BORDERS), EXP)
            if not log["hasPoints"]:
                self.funcEdit.setText("Function failed! Check the logs!")
                return
            if not log["hasPointsInRange"]:
                self.funcEdit.setText("Function failed! Out of range!")
                return
            if len(self.funcBank.keys()) < len(COLOR_BANK):  # Выбор цвета функции
                color = choice(self.funcColorLook)
                self.funcColorLook.remove(color)
            else:
                color = choice(self.colorBank)
            self.plotFunc(coords, color)
            self.funcBank[func] = coords, color
            if self.funcList.item(0).text() == "Empty!":
                self.funcList.clear()
            self.funcList.addItem("y = " + func)

    def plotFunc(self, coords: list[tuple[float, float] | None], color: QColor):
        canvas = self.canvasL.pixmap()
        self.painter.begin(canvas)
        self.pen.setColor(color)
        self.painter.setPen(self.pen)
        for p in coords:
            if p is None:
                continue
            self.drawPoint(p)
        self.canvasL.setPixmap(canvas)
        self.painter.end()

    def clear(self):
        canvas = QPixmap(*CANVAS_SIZE)
        canvas.fill(QColor('white'))
        self.canvasL.setPixmap(canvas)
        self.funcList.clear()
        self.funcList.addItem("Empty!")
        self.funcBank.clear()
        self.funcColorLook = self.colorBank.copy()
        self.funcEdit.clear()

    def setGraph(self):
        color = QColor("black")
        coords = self.XFuncData
        self.plotFunc(coords, color)
        self.funcBank["Xgraph"] = coords, color

    def drawPoint(self, coords: tuple[float, float]):
        self.painter.drawPoint(QPointF(*self.refCoords(coords)))

    def refCoords(self, coords: tuple[float, float]) -> tuple[float, float]:
        coords = (self.canvasL.width() // 2 + coords[0] * POINT_DIF, self.canvasL.height() // 2 - coords[1] * POINT_DIF)
        return coords


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
