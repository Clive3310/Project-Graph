from PyQt6.QtWidgets import QApplication, QMessageBox, QFileDialog, QMainWindow
import sys
from PIL import Image
from db_tools import addUser, checkUserPas, deleteUser
from views.RmainWin import MainWin
from views.RregWin import RegWin
from views.RlogWin import LogWin
from views.RproWin import ProWin
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
    def __init__(self):
        self.win = QMainWindow()
        self.username = None
        self.setupStarting()

    def startMain(self):
        if self.win:
            self.win.close()
        self.win = MainWin()
        self.setupMain()
        self.win.show()

    def startReg(self):
        if self.win:
            self.win.close()
        self.win = RegWin()
        self.setupReg()
        self.win.show()

    def startPro(self):
        if self.win:
            self.win.close()
        self.win = ProWin()
        self.setupPro()
        self.win.show()

    def setupPro(self):
        self.win.setFixedSize(self.win.size())

        pm = QPixmap(f"./res/{self.username}.png")
        if pm.isNull():
            print("User's image not found!")
            pm = QPixmap("./res/baseImg.png")
        self.win.imgLabel.setPixmap(pm)
        if self.username is None:
            user = "BaseName"
        else:
            user = self.username
        self.win.nameLabel.setText(user)
        self.win.backToMainButt.clicked.connect(self.startMain)
        self.win.leaveProphileButt.clicked.connect(self.startLogIn)
        self.win.deleteProphileButt.clicked.connect(self.deleteProSelf)

    def deleteProSelf(self):
        ans = QMessageBox.question(self.win, "Подтверждение", "Вы уверены что хотите безвозвратно удалить аккаунт?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if ans == QMessageBox.StandardButton.No:
            return

        try:
            deleteUser(self.username)
        except Exception as e:
            print(e)
            return

        self.startLogIn()

    def setupReg(self):
        self.win.setFixedSize(self.win.size())
        self.win.registrateButt.clicked.connect(self.registrate)
        self.win.logInLinkButt.clicked.connect(self.startLogIn)
        self.win.chooseImgPathButt.clicked.connect(self.chooseImg)

    def chooseImg(self):
        filepath = QFileDialog.getOpenFileName(self.win, "Выберите файл", filter="Images (*.png)")[0]

        if filepath:
            self.win.imgPathEdit.setText(filepath)

    def startLogIn(self):
        if self.win:
            self.win.close()
        self.win = LogWin()
        self.setupLog()
        self.win.show()

    def setupLog(self):
        self.win.setFixedSize(self.win.size())
        self.win.logButt.clicked.connect(self.logIn)
        self.win.regLinkButt.clicked.connect(self.startReg)

    def logIn(self):
        username = self.win.nameEdit.text().strip()
        password = self.win.passwordEdit.text().strip()

        if not (username and password):
            return

        ans = checkUserPas(username, password)
        if not ans:
            self.startMain()
            self.username = username
        else:
            self.win.errorLabel.setText("Неверный логин или пароль!")

    def registrate(self):
        username = self.win.nameEdit.text().strip()
        password = self.win.passwordEdit.text().strip()
        re_password = self.win.passwordConfirm.text().strip()
        img_path = self.win.imgPathEdit.text().strip()

        ncheck = checkUsername(username)
        if ncheck != "good":
            self.win.errorLabel.setText(ncheck)
            return
        pcheck = checkPassword(password, re_password)
        if pcheck != "good":
            self.win.errorLabel.setText(pcheck)
            return

        if img_path:
            try:
                img = Image.open(img_path)
            except Exception:
                self.win.errorLabel.setText("Не удалось загрузить картинку!")
                return
            if img.size != IMGLABELSIZE:
                self.win.errorLabel.setText("Картинка должна быть 128x128")
                return
            img.save(f"./res/{username}.{img_path.strip().split('.')[-1]}")
        self.win.errorLabel.setText("")

        error = addUser(username, password)
        if error is not None:
            self.win.errorLabel.setText(error)
            return
        self.win.nameEdit.clear()
        self.win.passwordEdit.clear()
        self.win.passwordConfirm.clear()
        self.win.imgPathEdit.clear()
        self.win.errorLabel.setText("Профиль зарегистрирован!")

    def setupMain(self):
        self.win.setFixedSize(*WIN_SIZE)
        self.win.setWindowIcon(QIcon("icon.png"))
        self.clear()
        self.setupMainBack()

    def setupStarting(self):
        self.XFuncData = getCoords("0", range(*RANGE_BORDERS), EXP)[0], QColor("black").rgb()
        self.YFuncData = [(0.0, round(x / EXP, PRESY)) for x in range(*RANGE_BORDERS)], QColor("black").rgb()
        self.funcBank = dict()  # {funcName: (coords, color)}
        self.colorBank = COLOR_BANK.copy()
        self.funcColorLook = self.colorBank.copy()
        self.pointWidth = POINT_WIDTH
        self.painter = QPainter()
        self.painter.setRenderHint(QPainter.RenderHint.Antialiasing)  # Вроде с этим чуть ровнее
        self.pen = QPen()
        self.pen.setWidth(self.pointWidth)

    def setupMainBack(self):
        self.win.btnPlot.clicked.connect(self.plotButt)
        self.win.btnClear.clicked.connect(self.clear)
        self.win.saveJSONb.clicked.connect(self.saveToJson)
        self.win.loadJSONb.clicked.connect(self.loadFromJson)
        self.win.prophileButtMain.clicked.connect(self.startPro)

    def saveToJson(self):
        filename = self.win.jsonFileNameEdit.text().strip()
        if filename:
            td = self.funcBank.copy()
            td.pop("Xgraph")
            td.pop("Ygraph")
            if not td:
                throwError("Empty canvas!")
                return
            saveToJson(td, filename)

    def loadFromJson(self):
        filename = QFileDialog.getOpenFileName(self.win, "Выберите файл", directory="./res",
                                               filter="JSON (*.json);;")[0]
        if filename:
            self.clear()
            self.funcBank = loadFromJson(filename)
            canvas = self.win.canvasL.pixmap()
            self.painter.begin(canvas)
            self.pen.setWidth(POINT_WIDTH)
            for func, data in self.funcBank.items():
                self.pen.setColor(QColor(data[1]))
                self.painter.setPen(self.pen)
                for p in data[0]:
                    self.drawPoint(p)
            self.funcBank["Xgraph"] = self.XFuncData[0], self.XFuncData[1]
            self.funcBank["Ygraph"] = self.YFuncData[0], self.YFuncData[1]
            self.win.canvasL.setPixmap(canvas)
            self.painter.end()

            inter_coords = self.getInterPoints()
            self.plotInterFunc(inter_coords)

            self.updateFuncList()

    def plotButt(self):
        func = self.win.funcEdit.text().strip()
        if func and func not in self.funcBank.keys():
            coords, log = getCoords(func, range(*RANGE_BORDERS), EXP)
            # Error checking
            if log["fatalError"]:
                throwError(log["fatalError"])
                return
            if not log["hasPoints"]:
                throwError("Function doesn't have points!")
                return
            if not log["hasPointsInRange"]:
                throwError("Function doesn't have points in range!")
                return
            if any([coords == i[0] for i in self.funcBank.values()]):
                throwError("Graph has function equivalent!")
                return
            if len(self.funcBank.keys()) < len(COLOR_BANK):  # Выбор цвета функции
                color = choice(self.funcColorLook)
                self.funcColorLook.remove(color)
            else:
                color = choice(self.colorBank)
            colorRgb = color.rgb()
            self.plotFunc(coords, colorRgb)
            self.funcBank[func] = coords, colorRgb

            inter_coords = self.getInterPoints()  # Точки пересечения
            self.plotInterFunc(inter_coords)

            if self.win.funcList.item(0).text() == "Empty!":
                self.win.funcList.clear()
            self.updateFuncList()

    def plotFunc(self, coords: list[tuple[float, float]], colorRgb: int):
        canvas = self.win.canvasL.pixmap()
        self.painter.begin(canvas)
        self.pen.setColor(QColor(colorRgb))
        self.pen.setWidth(POINT_WIDTH)
        self.painter.setPen(self.pen)
        for p in coords:
            self.drawPoint(p)
        self.win.canvasL.setPixmap(canvas)
        self.painter.end()

    def plotInterFunc(self, coords: list[tuple[float, float]]):
        canvas = self.win.canvasL.pixmap()
        self.painter.begin(canvas)
        self.pen.setColor(INTER_COLOR)
        self.pen.setWidth(POINT_WIDTH + 2)
        self.painter.setPen(self.pen)
        for p in coords:
            self.drawPoint(p)
        self.painter.end()
        self.win.canvasL.setPixmap(canvas)

    def clear(self):
        canvas = QPixmap(*CANVAS_SIZE)
        canvas.fill(QColor(CANVAS_COLOR))
        self.win.jsonFileNameEdit.clear()
        self.win.canvasL.setPixmap(canvas)
        self.win.funcList.clear()
        self.win.funcList.addItem("Empty!")
        self.funcBank.clear()
        self.funcColorLook = self.colorBank.copy()
        self.win.funcEdit.clear()
        self.setGraphs()

    def updateFuncList(self):
        self.win.funcList.clear()
        for func in self.funcBank.keys():
            if func not in ("Xgraph", "Ygraph"):
                self.win.funcList.addItem("y = " + func)

    def setGraphs(self):
        self.plotFunc(*self.XFuncData)
        self.funcBank["Xgraph"] = self.XFuncData[0], self.XFuncData[1]

        self.plotFunc(*self.YFuncData)
        self.funcBank["Ygraph"] = self.YFuncData[0], self.YFuncData[1]

        # Draw checks
        canvas = self.win.canvasL.pixmap()
        self.painter.begin(canvas)
        self.pen.setColor(QColor("black"))
        self.painter.setPen(self.pen)
        for x in range(-450, 500, 20):
            self.painter.drawLine(QPointF(x, self.win.canvasL.height() // 2 + CHECKS_SIZE),
                                  QPointF(x, self.win.canvasL.height() // 2 - CHECKS_SIZE))
        for y in range(-450, 500, 20):
            self.painter.drawLine(QPointF(self.win.canvasL.width() // 2 - CHECKS_SIZE, y),
                                  QPointF(self.win.canvasL.width() // 2 + CHECKS_SIZE, y))
        self.painter.end()
        self.win.canvasL.setPixmap(canvas)

    def drawPoint(self, coords: tuple[float, float]):
        self.painter.drawPoint(QPointF(*self.refCoords(coords)))

    def refCoords(self, coords: tuple[float, float]) -> tuple[float, float]:
        coords = (self.win.canvasL.width() // 2 + coords[0] * POINT_DIF,
                  self.win.canvasL.height() // 2 - coords[1] * POINT_DIF)
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
