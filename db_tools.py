import sqlite3

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
CREATEDATATABLE = """CREATE TABLE IF NOT EXISTS data
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
                         data
                         TEXT
                         NOT
                         NULL
                     );"""

INSERTUSER = """INSERT INTO users (username, password)
                VALUES (?, ?)"""
INSERTIMAGE = """INSERT INTO data (id, username, password)"""
DELETEUSER = """DELETE
                FROM users
                WHERE username = ?"""
CHECKUSERPASSWORD = """SELECT username
                       FROM users
                       WHERE username = ?
                         AND password = ?"""


def setupdb():
    con = sqlite3.connect(r"C:\timoha\PyCharm\projectCalc\res\users.sqlite")
    cur = con.cursor()
    cur.execute(CREATEUSERTABLE)
    cur.execute(CREATEDATATABLE)
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
    con.commit()
    con.close()
    return None


def checkUserPas(username, password):
    con = sqlite3.connect(r"C:\timoha\PyCharm\projectCalc\res\users.sqlite")
    cur = con.cursor()
    try:
        ans = cur.execute(CHECKUSERPASSWORD, (username, password)).fetchone()
    except sqlite3.OperationalError as e:
        setupdb()
        ans = cur.execute(CHECKUSERPASSWORD, (username, password)).fetchone()
    con.close()
    return not ans


if __name__ == "__main__":
    setupdb()
