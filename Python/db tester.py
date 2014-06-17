import mysql.connector

conn = mysql.connector.Connect(host='localhost',user='bi2_pg6',
                        password='blaat1234',database='InfiRap')

c = conn.cursor()

f=open("/home/bi2_pg6/public_html/Inficio Raptum/Python/test2.txt",'w')
c.execute ("""select * from Article""")

for row in c:
        f.write(row[3])
        f.write("\n")

c.close()
f.close()
