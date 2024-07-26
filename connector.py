import mysql.connector as sql

def sql_cnnection(id,name,age,mobilenumber,mail):
  mydb = sql.connect(
    host="localhost",
    port=3306,
    user="root",
    password="",
    database="mydatabase"
  )

  mycursor = mydb.cursor()

  sql1 = "INSERT INTO user (id,name,age,mobilenumber,mail) VALUES (%s,%s,%s,%s,%s)"
  val = (id,name,age,mobilenumber,mail)
  mycursor.execute(sql1, val)

  mydb.commit()

  print(mycursor.rowcount, "record inserted.")
  return 'ok'

def sql_update(id,name,age,mobilenumber,mail,):
  mydb = sql.connect(
    host="localhost",
    port=3306,
    user="root",
    password="",
    database="mydatabase"
  )

  mycursor = mydb.cursor()
  sql2 = "UPDATE user SET name = %s, age = %s, mobilenumber = %s, mail = %s WHERE id = %s"

  val = (name, age, mobilenumber, mail, id)

  mycursor.execute(sql2, val)


  mydb.commit()

  print(mycursor.rowcount, "record(s) updated")
  return 'ok'


def sql_delete(id,):
  mydb = sql.connect(
    host="localhost",
    port=3306,
    user="root",
    password="",
    database="mydatabase"
  )

  mycursor = mydb.cursor()
  sql3 = "DELETE FROM user WHERE id = %s"

  val = (id,)

  mycursor.execute(sql3, val)

  mydb.commit()

  print(mycursor.rowcount, "record(s) deleted")
  return 'ok'

def fetch_data():
    mydb = sql.connect(
    host="localhost",
    port=3306,
    user="root",
    password="",
    database="mydatabase"
    )
    mycursor=mydb.cursor()
    
    mycursor.execute("SELECT IDno, Name, Age, MobileNumber, Mail FROM users")
    data = mycursor.fetchall()
    conn.close()
    mydb.commit()
    print("ok")
    return data
