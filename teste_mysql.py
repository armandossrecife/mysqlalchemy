import mysql.connector

mydb = mysql.connector.connect(
    host="localhost", 
    user="armando",
    password="skyinfo", 
    database="promocity"
)

mycursor = mydb.cursor()

mycursor.execute("select * from users;")

for each in mycursor:
    print(each)