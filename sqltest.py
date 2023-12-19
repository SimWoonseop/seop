import pymysql
from PyQt5.QtWidgets import *
conn = pymysql.connect(host='127.0.0.1', user='root', password='0000', db='studentDB', charset='utf8', cursorclass=pymysql.cursors.DictCursor, autocommit=False)
tempconn = pymysql.connect(host='127.0.0.1', user='root', password='0000', db='studentDB', charset='utf8', cursorclass=pymysql.cursors.DictCursor, autocommit=False)
cur = conn.cursor()
new_cur = tempconn.cursor()

def openDB():
  sql = "select * from usertable"
  cur.execute(sql)
  result = cur.fetchall()

  total_DB = {}
  for row in result:
    total_DB[row['id']] = row['userName']
  
  return total_DB
                  
def intoDB(id, name):
  sql = "insert into usertable (id, userName) values(%s, %s)"
  val = (id, name)
  cur.execute(sql, val)

def deleteDB(id):
  sql = "delete from userTable genders where id=%s"
  val = (id)
  cur.execute(sql, val)

def changeDB(name, id):
  sql = "update userTable set userName=%s where id=%s"
  val = (name, id)
  cur.execute(sql, val)

def saveDB(message):
  if message == QMessageBox.Yes:
    conn.commit()
  else:
    pass

def DB(total):
  sql = "select * from usertable"
  new_cur.execute(sql)
  result = new_cur.fetchall()

  total_DB = {}
  for row in result:
    total_DB[row['id']] = row['userName']

  if total == total_DB:
    return True
  else:
    return False

def closeDB():
  conn.close()