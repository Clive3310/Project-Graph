from PyQt6.QtGui import QColor
import json
from math import sin, cos, pi

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
MIN_PASSWORD_LEN, MAX_PASSWORD_LEN = 5, 30
MIN_USERNAME_LEN, MAX_USERNAME_LEN = 5, 30
IMGLABELSIZE = 128, 128


def getCoords(func: str, rng: range, exp: int) -> tuple[list[tuple[float, float]], dict]:
    coords = []
    log = {"hasPoints": False, "hasPointsInRange": False, "fatalError": False}
    if "^" in func:
        func = func.replace("^", "**")
    for x in rng:
        x = round(x / exp, PRESX)
        y = 0.0
        try:
            y = round(eval(func), PRESY)
        except ZeroDivisionError as e:
            print(f"Function '{func}' dropped with: {x, y}")
            print(f"---- {e}\n")
            continue
        except Exception as e:
            log["fatalError"] = e
            return coords, log
        if 0 <= CANVAS_SIZE[1] // 2 - y * POINT_DIF <= CANVAS_SIZE[1]:
            log["hasPointsInRange"] = True
        coords.append((float(x), float(y)))
        log["hasPoints"] = True

    return coords, log


def saveToJson(dictionary: dict, filename: str):
    with open(f"res/{filename}.json", 'w') as outfile:
        json.dump(dictionary, outfile)


def loadFromJson(filename: str):
    with open(filename, 'r') as json_file:
        dictionary = json.load(json_file)
        return dictionary


def checkPassword(password: str, re_password: str):
    if len(password) < MIN_PASSWORD_LEN:
        return "Пароль слишком короткий!"
    if len(password) > MAX_PASSWORD_LEN:
        return "Пароль слишком длинный!"
    if password != re_password:
        return "Пароли не совпадают!"
    return "good"


def checkUsername(username: str):
    if len(username) < MIN_USERNAME_LEN:
        return "Имя слишком короткое!"
    if len(username) > MAX_USERNAME_LEN:
        return "Имя слишком длинное!"
    if not username.replace(" ", "").isalpha():
        return "Имя должно содержать только буквы!"
    return "good"
