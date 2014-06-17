import itertools
import mysql.connector

conn = mysql.connector.Connect(host='localhost',user='bi2_pg6',
                        password='blaat1234',database='InfiRap')

c1 = conn.cursor()

f=open("/home/bi2_pg6/public_html/Inficio Raptum/Python/edges.3j",'w')
n=open("/home/bi2_pg6/public_html/Inficio Raptum/Python/nodes.3j",'w')

c1.execute("""SELECT chemical_name FROM Compound""")
compoundList = []
dic = {}
for row in c1:
    compoundList.append(row[0])

i=0
count = 0
pubList = []
for i in compoundList:
    count += 1
    statement1 = """SELECT  `Article_ID` 
    FROM  `Compound-Article` 
    WHERE Compound_Sysname =  '"""+i+"""'"""
    c1.execute(statement1)
    for row in c1:
        pubList.append(row)
    n.write(">")
    n.write(str(count))
    n.write("\n*")
    n.write(str(i))
    n.write(" \n#")
    n.write(str(len(pubList)))
    n.write("\n@")
    for a in pubList:
        n.write(str(a).replace('u','').replace("'", '').replace('(', '').replace(')','').replace(",,", ','))
    n.write("\n+\n")
    pubSet = set(pubList)        
    dic[count] = pubSet
    pubList = []

countCompound = count
c1.execute("""SELECT latin_surname FROM Organism""")
organismsurnameList = []

for row in c1:
    organismsurnameList.append(row[0])
    
c1.execute("""SELECT latin_prefix FROM Organism""")
organismprefixList = []

for row in c1:
    organismprefixList.append(row[0])


i=0
pubList = []
n.write(": \n")
for (i, j) in zip(organismprefixList, organismsurnameList):
    count += 1
    statement1 = """SELECT  `Article_ID` 
    FROM  `Article-Organism` 
    WHERE Organism_surname =  '"""+j+"""'"""
    c1.execute(statement1)
    for row in c1:
        pubList.append(row)
    n.write(">")
    n.write(str(count))
    n.write("\n*")
    n.write(str(i)+" "+str(j))
    n.write(" \n#")
    n.write(str(len(pubList)))
    n.write("\n@")
    for a in pubList:
        n.write(str(a).replace('u','').replace("'", '').replace('(', '').replace(')','').replace(",,", ','))
    n.write("\n+\n")
    pubSet = set(pubList)        
    dic[count] = pubSet
    pubList = []

vergelijk = list(itertools.combinations(dic.values(), 2))
vergelijknamen = list(itertools.combinations(dic.keys(), 2))
for (z, y) in zip(vergelijk, vergelijknamen):
        set1 = z[0]
        naam1 = y[0]
        set2 = z[1]
        naam2 = y[1]
        if naam1 <= countCompound and naam2 > countCompound:
            totaal = len(set1 & set2)
            f.write(">" )
            f.write(str(y[0]))
            f.write("\n*")
            f.write(str(y[1]))
            f.write("\n#")
            f.write(str(set1 & set2).replace("set()", "").replace("{","").replace("}","").replace("'","").replace("set(",'').replace(')','').replace("(","").replace("]","").replace("[",""))
            f.write("\n@")
            f.write(str(totaal))
            f.write("\n%\n")
c1.close()
f.close()
n.close()
