import pymysql
conn = pymysql.connect(host='127.0.0.1', user='root', password='0000', db='studentDB', charset='utf8')
cur = conn.cursor()

def intoDB(id, name):
  sql = "insert into usertable values(%s, %s)"
  val = (id, name)
  cur.execute(sql, val)
  conn.commit()

def deleteDB(id):
  sql = "delete from userTable genders where id=%s"
  val = (id)
  cur.execute(sql, val)
  conn.commit()
