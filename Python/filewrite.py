#!/usr/bin/python
import MySQLdb
file = open("/home/bi2_pg6/public_html/Inficio Raptum/Python/dbarticle.txt",'w')

db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="bi2_pg6", # your username
                      passwd="blaat1234", # your password
                      db="InfiRap") # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor() 

# Use all the SQL you like
cur.execute("SELECT * FROM Article")

# print all the first cell of all the rows
for row in cur.fetchall():
    file.write(row[0])

file.close()
