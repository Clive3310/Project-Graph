from PyQt6.QtWidgets import QApplication, QMessageBox
import sys
from PyUIs.RmainWin import MainWin
from logic import *
from PyQt6.QtGui import QIcon, QPainter, QPixmap, QPen, QColor
from PyQt6.QtCore import QPointF
from random import choice


def throwError(errorText):
    win = QMessageBox()
    win.setWindowTitle("Error")
    win.setText(errorText.__str__())
    win.exec()


class Controller:
    def startMain(self):
        self.mWin = MainWin()
        self.setup()
        self.mWin.show()

    def setup(self):
        self.mWin.setFixedSize(*WIN_SIZE)
        self.mWin.setWindowIcon(QIcon("./res/icon.png"))
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
        self.mWin.btnPlot.clicked.connect(self.plotButt)
        self.mWin.btnClear.clicked.connect(self.clear)

    def plotButt(self):
        func = self.mWin.funcEdit.text().strip()
        if func and func not in self.funcBank.keys():
            coords, log = getCoords(func, range(*RANGE_BORDERS), EXP)
            if log["fatalError"]:
                throwError(log["fatalError"])
                return
            if not log["hasPoints"]:
                throwError("Function doesn't have points!")
                return
            if not log["hasPointsInRange"]:
                throwError("Function doesn't have points in range!")
                return
            if len(self.funcBank.keys()) < len(COLOR_BANK):  # Выбор цвета функции
                color = choice(self.funcColorLook)
                self.funcColorLook.remove(color)
            else:
                color = choice(self.colorBank)
            self.plotFunc(coords, color)
            self.funcBank[func] = coords, color

            inter_coords = self.getInterPoints()  # Точки пересечения
            self.plotInterFunc(inter_coords)

            if self.mWin.funcList.item(0).text() == "Empty!":
                self.mWin.funcList.clear()
            self.mWin.funcList.addItem("y = " + func)

    def plotFunc(self, coords: list[tuple[float, float]], color: QColor):
        canvas = self.mWin.canvasL.pixmap()
        self.painter.begin(canvas)
        self.pen.setColor(color)
        self.pen.setWidth(POINT_WIDTH)
        self.painter.setPen(self.pen)
        for p in coords:
            self.drawPoint(p)
        self.mWin.canvasL.setPixmap(canvas)
        self.painter.end()

    def plotInterFunc(self, coords: list[tuple[float, float]]):
        canvas = self.mWin.canvasL.pixmap()
        self.painter.begin(canvas)
        self.pen.setColor(INTER_COLOR)
        self.pen.setWidth(POINT_WIDTH + 2)
        self.painter.setPen(self.pen)
        for p in coords:
            self.drawPoint(p)
        self.painter.end()
        self.mWin.canvasL.setPixmap(canvas)

    def clear(self):
        canvas = QPixmap(*CANVAS_SIZE)
        canvas.fill(QColor(CANVAS_COLOR))
        self.mWin.canvasL.setPixmap(canvas)
        self.mWin.funcList.clear()
        self.mWin.funcList.addItem("Empty!")
        self.funcBank.clear()
        self.funcColorLook = self.colorBank.copy()
        self.mWin.funcEdit.clear()
        self.setGraphs()

    def setGraphs(self):
        self.plotFunc(*self.XFuncData)
        self.funcBank["Xgraph"] = self.XFuncData[0], self.XFuncData[1]

        self.plotFunc(*self.YFuncData)
        self.funcBank["Ygraph"] = self.YFuncData[0], self.YFuncData[1]

        canvas = self.mWin.canvasL.pixmap()
        self.painter.begin(canvas)
        self.pen.setColor(QColor("black"))
        self.painter.setPen(self.pen)
        for x in range(-450, 500, 20):
            self.painter.drawLine(QPointF(x, self.mWin.canvasL.height() // 2 + CHECKS_SIZE),
                                  QPointF(x, self.mWin.canvasL.height() // 2 - CHECKS_SIZE))
        for y in range(-450, 500, 20):
            self.painter.drawLine(QPointF(self.mWin.canvasL.width() // 2 - CHECKS_SIZE, y),
                                  QPointF(self.mWin.canvasL.width() // 2 + CHECKS_SIZE, y))
        self.painter.end()
        self.mWin.canvasL.setPixmap(canvas)

    def drawPoint(self, coords: tuple[float, float]):
        self.painter.drawPoint(QPointF(*self.refCoords(coords)))

    def refCoords(self, coords: tuple[float, float]) -> tuple[float, float]:
        coords = (self.mWin.canvasL.width() // 2 + coords[0] * POINT_DIF,
                  self.mWin.canvasL.height() // 2 - coords[1] * POINT_DIF)
        return coords

    def getInterPoints(self) -> list[tuple[float, float]]:  # Получить все пересечения функций
        allPoints = set()
        goodPoints = set()
        for func, data in self.funcBank.items():
            points = list(map(lambda p: (round(p[0], 2), round(p[1], 2)), data[0]))
            # Считать точки пересечения с большим 'разрешением'
            goodPoints = goodPoints.union(allPoints.intersection(points))
            allPoints = allPoints.union(points)

        return list(goodPoints)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = Controller()
    controller.startMain()
    sys.exit(app.exec())
