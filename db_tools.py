import sqlite3

from logic import refactorVarsTo, refactorFuncsTo

CREATEUSERTABLE = """CREATE TABLE IF NOT EXISTS users
                     (
                         id
                         INTEGER
                         PRIMARY
                         KEY
                         AUTOINCREMENT
                         UNIQUE
                         NOT
                         NULL,
                         username
                         TEXT
                         UNIQUE
                         NOT
                         NULL,
                         password
                         TEXT
                         NOT
                         NULL
                     );"""
CREATEUSERVARSTABLE = """CREATE TABLE IF NOT EXISTS userVars
                         (
                             id
                             INTEGER
                             PRIMARY
                             KEY
                             AUTOINCREMENT
                             UNIQUE
                             NOT
                             NULL,
                             username
                             TEXT
                             NOT
                             NULL
                             UNIQUE,
                             variables
                             TEXT
                             NOT
                             NULL
                         );"""
CREATEUSERFUNCSTABLE = """CREATE TABLE IF NOT EXISTS userFuncs
                          (
                              id
                              INTEGER
                              PRIMARY
                              KEY
                              AUTOINCREMENT
                              UNIQUE
                              NOT
                              NULL,
                              username
                              TEXT
                              UNIQUE
                              NOT
                              NULL,
                              functions
                              TEXT
                              NOT
                              NULL
                          );"""
INSERTUSER = """INSERT INTO users (username, password)
                VALUES (?, ?)"""
DELETEUSER = """DELETE
                FROM users
                WHERE username = ?"""
CHECKUSERPASSWORD = """SELECT username
                       FROM users
                       WHERE username = ?
                         AND password = ?"""
SETUPVARS = """INSERT INTO userVars(username, variables)
               VALUES (?, ?)"""
SETUPFUNCS = """INSERT INTO userFuncs(username, functions)
                VALUES (?, ?)"""
UPDATEVARS = """UPDATE userVars
                SET variables = ?
                WHERE username = ?"""
UPDATEFUNCS = """UPDATE userFuncs
                 SET functions = ?
                 WHERE username = ?"""
DELETEVARS = """DELETE
                FROM userVars
                WHERE username = ?"""
DELETEFUNCS = """DELETE
                 FROM userFuncs
                 WHERE username = ?"""
GETUSERV = """SELECT variables FROM userVars WHERE username = ?"""
GETUSERF = """SELECT functions FROM userFuncs WHERE username = ?"""


def setupdb():
    con = sqlite3.connect(r"C:\timoha\PyCharm\projectCalc\res\users.sqlite")
    cur = con.cursor()
    cur.execute(CREATEUSERTABLE)
    cur.execute(CREATEUSERVARSTABLE)
    cur.execute(CREATEUSERFUNCSTABLE)
    con.commit()
    con.close()


def addUser(username, password):
    con = sqlite3.connect(r"C:\timoha\PyCharm\projectCalc\res\users.sqlite")
    cur = con.cursor()
    try:
        cur.execute(INSERTUSER, (username, password))
    except sqlite3.OperationalError as e:
        setupdb()
        cur.execute(INSERTUSER, (username, password))
    except sqlite3.IntegrityError as e:
        con.close()
        return f"Имя уже занято: {e}"
    cur.execute(SETUPVARS, (username, ""))
    cur.execute(SETUPFUNCS, (username, ""))
    con.commit()
    con.close()
    return None


def deleteUser(username):
    con = sqlite3.connect(r"C:\timoha\PyCharm\projectCalc\res\users.sqlite")
    cur = con.cursor()
    try:
        cur.execute(DELETEUSER, (username,))
    except sqlite3.OperationalError as e:
        setupdb()
        cur.execute(DELETEUSER, (username,))
    except Exception as e:
        con.close()
        return f"Error: {e}"
    cur.execute(DELETEVARS, (username,))
    cur.execute(DELETEFUNCS, (username,))
    con.commit()
    con.close()
    return None


def checkUserPas(username: str, password: str):
    con = sqlite3.connect(r"C:\timoha\PyCharm\projectCalc\res\users.sqlite")
    cur = con.cursor()
    try:
        ans = cur.execute(CHECKUSERPASSWORD, (username, password)).fetchone()
    except sqlite3.OperationalError as e:
        setupdb()
        ans = cur.execute(CHECKUSERPASSWORD, (username, password)).fetchone()
    con.close()
    return not ans


def updateData(username: str, varbs: dict[str, str], funcs: dict[str, str]):
    con = sqlite3.connect(r"C:\timoha\PyCharm\projectCalc\res\users.sqlite")
    cur = con.cursor()
    dataVarbs = refactorVarsTo(varbs)
    dataFuncs = refactorFuncsTo(funcs)
    try:
        cur.execute(UPDATEVARS, (dataVarbs, username))
    except sqlite3.OperationalError as e:
        setupdb()
        cur.execute(UPDATEVARS, (dataVarbs, username))
    except Exception as e:
        print(e)
        return
    cur.execute(UPDATEFUNCS, (dataFuncs, username))
    con.commit()
    con.close()
    return


def deleteDataRows(username: str):
    con = sqlite3.connect(r"C:\timoha\PyCharm\projectCalc\res\users.sqlite")
    cur = con.cursor()
    try:
        cur.execute(DELETEVARS, (username, ))
    except sqlite3.OperationalError as e:
        setupdb()
        cur.execute(DELETEVARS, (username, ))
    except Exception as e:
        print(e)
        return
    cur.execute(DELETEFUNCS, (username, ))
    con.commit()
    con.close()
    return


def getUserVF(username: str):
    con = sqlite3.connect(r"C:\timoha\PyCharm\projectCalc\res\users.sqlite")
    cur = con.cursor()
    try:
        varbs = cur.execute(GETUSERV, (username,)).fetchone()[0]
    except sqlite3.OperationalError as e:
        setupdb()
        varbs = cur.execute(GETUSERV, (username,)).fetchone()[0]
    except Exception as e:
        print(e)
        return
    funcs = cur.execute(GETUSERF, (username,)).fetchone()[0]
    con.commit()
    con.close()
    return varbs, funcs


if __name__ == "__main__":
    setupdb()
