import sys
import os
import mysql.connector
from mysql.connector import Error

r=0

try:
     conn = mysql.connector.connect(
             host=os.environ['SDI_DATABASE_HOST'],
             database=os.environ['SDI_DATABASE_NAME'],
             user=os.environ['SDI_DATABASE_USER'],
             password=os.environ['SDI_DATABASE_PASSWORD'])
     if conn.is_connected():
          cursor = conn.cursor()
          cursor.execute("select database();")
          record = cursor.fetchall()
          print ("Connected to database: ", record)
     if(conn.is_connected()):
          cursor.close()
          conn.close()
except Error as e:
     print ("No connection yet", e)
     r=1
finally:
     sys.exit(r)


