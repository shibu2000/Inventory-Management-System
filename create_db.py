import sqlite3


def create_db():
    con = sqlite3.connect(database=r'ims.db')
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS EMPLOYEE(EMPID INTEGER PRIMARY KEY AUTOINCREMENT, NAME text, EMAIL text, GENDER text, CONTACT text, DOB text, DOJ text, PASSWORD text, UTYPE text, ADDRESS text, SALARY text)")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS SUPPLIER(INVOICE INTEGER PRIMARY KEY AUTOINCREMENT, NAME text, CONTACT text, DESCRIPTION text)")
    con.commit()

    cur.execute(
        "CREATE TABLE IF NOT EXISTS CATEGORY(CID INTEGER PRIMARY KEY AUTOINCREMENT, NAME text)")
    con.commit()

    cur.execute(
        "CREATE TABLE IF NOT EXISTS PRODUCT(P_ID INTEGER PRIMARY KEY AUTOINCREMENT,CATEGORY text, SUPPLIER text ,NAME text, PRICE INTEGER, QTY INTEGER,STATUS text)")
    con.commit()


create_db()
