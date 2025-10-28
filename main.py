from PyQt6.QtCore import QPointF
from PyQt6.QtWidgets import QApplication, QMainWindow
import sys
from random import choice
from math import sin, cos, pi  # Just in case...
from PyQt6.QtGui import QColor, QPainter, QPixmap, QPen, QIcon
from Ui_file import Ui_windowMain


WIN_SIZE = 915, 540
CANVAS_SIZE = 500, 500
CANVAS_COLOR = 0xdfdfdf
# RANGE_BORDERS = -12500, 12501 - Реальная граница
RANGE_BORDERS = -12450, 12450
EXP = 1000
COLOR_BANK = [QColor('red'), QColor('blue'), QColor('green'), QColor('purple'), QColor('magenta')]
INTER_COLOR = QColor("black")
POINT_DIF = 20
POINT_WIDTH = 2
CHECKS_SIZE = 2
PRESX = 4
PRESY = 4


# TODO Иконки для tab'ов, Ui и функционал 2 вкладки


def getCoords(func: str, rng: range, exp: int) -> tuple[list[tuple[float, float]], dict[str, bool]]:
    coords = []
    log = {"hasPoints": False, "hasPointsInRange": False}
    if "^" in func:
        func = func.replace("^", "**")
    for x in rng:
        x = round(x / exp, PRESX)
        # if 0 < x < 1.3:
        #     print(x, round(eval(func), 2), func)
        y = 0.0
        try:
            y = round(eval(func), PRESY)
        except Exception as e:
            print(f"Function '{func}' dropped with: {x, y}")
            print(f"---- {e}\n")
            continue
        if 0 <= CANVAS_SIZE[1] // 2 - y * POINT_DIF <= CANVAS_SIZE[1]:
            log["hasPointsInRange"] = True
        coords.append((float(x), float(y)))
        log["hasPoints"] = True
    return coords, log


class MainWindow(QMainWindow, Ui_windowMain):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setup()

    def setup(self):
        self.setFixedSize(*WIN_SIZE)
        self.setWindowIcon(QIcon("./res/icon.png"))
        self.XFuncData = getCoords("0", range(*RANGE_BORDERS), EXP)[0], QColor("black")
        self.YFuncData = [(0.0, round(x / EXP, PRESY)) for x in range(*RANGE_BORDERS)], QColor("black")
        self.funcBank = dict()  # {funcName: (coords, color)}
        self.colorBank = COLOR_BANK.copy()
        self.funcColorLook = self.colorBank.copy()
        self.pointWidth = POINT_WIDTH
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
        self.getUnPoints()
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

            inter_coords = self.getUnPoints()  # Точки пересечения
            self.plotInterFunc(inter_coords)

            if self.funcList.item(0).text() == "Empty!":
                self.funcList.clear()
            self.funcList.addItem("y = " + func)

    def plotFunc(self, coords: list[tuple[float, float]], color: QColor):
        canvas = self.canvasL.pixmap()
        self.painter.begin(canvas)
        self.pen.setColor(color)
        self.pen.setWidth(POINT_WIDTH)
        self.painter.setPen(self.pen)
        for p in coords:
            self.drawPoint(p)
        self.canvasL.setPixmap(canvas)
        self.painter.end()

    def plotInterFunc(self, coords: list[tuple[float, float]]):
        print(sorted(coords))
        canvas = self.canvasL.pixmap()
        self.painter.begin(canvas)
        self.pen.setColor(INTER_COLOR)
        self.pen.setWidth(POINT_WIDTH + 2)
        self.painter.setPen(self.pen)
        for p in coords:
            self.drawPoint(p)
        self.painter.end()
        self.canvasL.setPixmap(canvas)

    def clear(self):
        canvas = QPixmap(*CANVAS_SIZE)
        canvas.fill(QColor(CANVAS_COLOR))
        self.canvasL.setPixmap(canvas)
        self.funcList.clear()
        self.funcList.addItem("Empty!")
        self.funcBank.clear()
        self.funcColorLook = self.colorBank.copy()
        self.funcEdit.clear()
        self.setGraphs()

    def setGraphs(self):
        self.plotFunc(*self.XFuncData)
        self.funcBank["Xgraph"] = self.XFuncData[0], self.XFuncData[1]

        self.plotFunc(*self.YFuncData)
        self.funcBank["Ygraph"] = self.YFuncData[0], self.YFuncData[1]

        canvas = self.canvasL.pixmap()
        self.painter.begin(canvas)
        self.pen.setColor(QColor("black"))
        self.painter.setPen(self.pen)
        for x in range(-450, 500, 20):
            self.painter.drawLine(QPointF(x, self.canvasL.height() // 2 + CHECKS_SIZE),
                                  QPointF(x, self.canvasL.height() // 2 - CHECKS_SIZE))
        for y in range(-450, 500, 20):
            self.painter.drawLine(QPointF(self.canvasL.width() // 2 - CHECKS_SIZE, y),
                                  QPointF(self.canvasL.width() // 2 + CHECKS_SIZE, y))
        self.painter.end()
        self.canvasL.setPixmap(canvas)

    def drawPoint(self, coords: tuple[float, float]):
        self.painter.drawPoint(QPointF(*self.refCoords(coords)))

    def refCoords(self, coords: tuple[float, float]) -> tuple[float, float]:
        coords = (self.canvasL.width() // 2 + coords[0] * POINT_DIF, self.canvasL.height() // 2 - coords[1] * POINT_DIF)
        return coords

    def getUnPoints(self) -> list[tuple[float, float]]:  # Получить все пересечения функций
        allPoints = set()
        goodPoints = set()
        for func, data in self.funcBank.items():
            points = list(map(lambda p: (round(p[0], 3), round(p[1], 3)), data[0]))
            # Считать точки пересечения с большим 'разрешением'
            goodPoints = goodPoints.union(allPoints.intersection(points))
            allPoints = allPoints.union(points)

        return list(goodPoints)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
