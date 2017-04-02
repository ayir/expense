import psycopg2 as pg
import os
import urllib.parse as urlparse


url = urlparse.urlparse(os.environ['DATABASE_URL'])


def get_connection():
    conn = pg.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port)
    return conn


def create_db():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE USERS
        (USERID       TEXT    UNIQUE    NOT Null,
         NAME           TEXT    NOT NULL,
         PASSWORD        TEXT);''')
        print ("Table created successfully")
        cursor.execute('''CREATE TABLE USER_DATA
         (USERID       TEXT   REFERENCES USERS(USERID)  NOT Null,
            CATEGORIES           TEXT   UNIQUE   NOT NULL,
             PRICE            INT     NOT NULL,
            DESCRIPTION        TEXT);''')
        connection.commit()
        connection.close()
    except Exception as error:
        return error


def insert_categories(USER, CATEGORIES, PRICE, DESCRIPTION):
    connection = get_connection()
    cursor = connection.cursor()
    print ("cur is created")
    query = """INSERT INTO USER_DATA(USERID,CATEGORIES,PRICE,DESCRIPTION) VALUES('%s', '%s', %s, '%s');"""
    query = query % (
        USER, CATEGORIES, PRICE, DESCRIPTION)
    print (query)
    cursor.execute(query)
    connection.commit()
    print ("Records created successfully")
    connection.close()


def category_alreadyexits(USER, CATEGORIES, PRICE, DESCRIPTION):
    connection = get_connection()
    cursor = connection.cursor()
    query = """SELECT USERID from USER_DATA where CATEGORIES='%s';"""
    query = query % (CATEGORIES, )
    cursor.execute(query)
    rows = cursor.fetchall()
    print (rows)
    try:
        if (len(rows) == 0):
            insert_categories(USER, CATEGORIES, PRICE, DESCRIPTION)
        else:
            return 1
    except Exception as error:
        return error


def filter_user_chart(USER):
    connection = get_connection()
    cursor = connection.cursor()
    fetch_db = """SELECT CATEGORIES,SUM(PRICE) FROM USER_DATA WHERE USERID='%s' GROUP BY CATEGORIES"""
    fetch_db = fetch_db % (USER)
    cursor.execute(fetch_db)
    rows = cursor.fetchall()
    for row in rows:
        print ("categories", row[0], type(row[0]))
        print ("price = ", row[1])
    print ("Operation done successfully")
    cursor.close()
    return rows


def filter_user_data(USER):
    connection = get_connection()
    cursor = connection.cursor()
    fetch_db = """SELECT USERID, CATEGORIES, PRICE, DESCRIPTION  from USER_DATA where USERID='%s'"""
    fetch_db = fetch_db % (USER)
    cursor.execute(fetch_db)
    rows = cursor.fetchall()
    for row in rows:
        print ("User ID = ", row[0])
        print ("Your Name = ", row[1])      
        print ("Password = ", row[2], "\n")
    print ("Operation done successfully")
    cursor.close()
    return rows


def insert_db(USER, NAME, PASSWORD):
    connection = get_connection()
    cursor = connection.cursor()
    print ("cur is created")
    query = """INSERT INTO USERS(USERID,NAME,PASSWORD) VALUES('%s', '%s', '%s');"""
    query = query % (
        USER, NAME, PASSWORD)
    print (query)
    cursor.execute(query)
    connection.commit()
    print ("Records created successfully")
    connection.close()


def user_alreadyexits(USER,NAME,PASSWORD):
    if not USER:
        return 1
    elif not NAME:
        return 1
    elif not PASSWORD:
        return 1
    connection = get_connection()
    cursor = connection.cursor()
    query = """SELECT USERID from USERS where USERID='%s';"""
    query = query % (USER, )
    cursor.execute(query)
    rows = cursor.fetchall()
    print (rows)
    try:
        if (len(rows) == 0):
            insert_db(USER, NAME,PASSWORD)
        else:
            return 1
    except Exception as error:
        return error
    connection.close()


def authenticate(username, password):
    connection = get_connection()
    cursor = connection.cursor()
    query = """SELECT USERID, PASSWORD from USERS where USERID='%s' and PASSWORD='%s';"""
    query = query % (username, password)
    cursor.execute(query)
    rows = cursor.fetchall()
    print (rows)
    try:
        if (rows[0][0] == username) and (rows[0][1] == password):
            return 1
        else:
            return 0
    except Exception as error:
        return error
    connection.close()
