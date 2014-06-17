import itertools
import mysql.connector


def index(req, Substance):
    conn = mysql.connector.Connect(host='localhost',user='bi2_pg6',
                            password='blaat1234',database='InfiRap')

    c1 = conn.cursor()
    f=open("/home/bi2_pg6/public_html/Inficio Raptum/Python/edgesSearch.3j",'w')
    n=open("/home/bi2_pg6/public_html/Inficio Raptum/Python/nodesSearch.3j",'w')
    compoundList = []
    dic = {}
    i=0
    count = 0
    pubList = []
    checkList = []
    statement1 = """SELECT  `chemical_name` 
    FROM  `Compound` 
    WHERE chemical_name =  '"""+Substance+"""'"""
    c1.execute(statement1)
    for row in c1:
        checkList.append(row)
        checkString = str(checkList).replace("u",'').replace("{","").replace("}","").replace("'","").replace("set(",'').replace(')','').replace("(","").replace("]","").replace("[","")
        if checkString != None:
            compound(Substance)
            
    statement2 = """SELECT  `latin_prefix` 
    FROM  `Organism` 
    WHERE latin_prefix =  '"""+Substance+"""'"""
    c1.execute(statement2)
    for row in c1:
        checkList.append(row)
        checkString = str(checkList).replace("u",'').replace("{","").replace("}","").replace("'","").replace("set(",'').replace(')','').replace("(","").replace("]","").replace("[","")
        if checkString != None:
            organism(Substance)
            


    c1.close()
    f.close()
    n.close()

def compound(Substance):
    conn = mysql.connector.Connect(host='localhost',user='bi2_pg6',
                            password='blaat1234',database='InfiRap')

    c1 = conn.cursor()
    f=open("/home/bi2_pg6/public_html/Inficio Raptum/Python/edgesSearch.3j",'w')
    n=open("/home/bi2_pg6/public_html/Inficio Raptum/Python/nodesSearch.3j",'w')
    dic = {}
    i=0
    count = 0
    pubList = []
    statement1 = """SELECT  `Article_ID` 
    FROM  `Compound-Article` 
    WHERE Compound_Sysname =  '"""+Substance+"""'"""
    c1.execute(statement1)
    for row in c1:
        pubList.append(row)
    n.write(">")
    n.write(str(count))
    n.write("\n*")
    n.write(str(Substance))
    n.write(" \n#")
    n.write(str(len(pubList)))
    n.write("\n@")
    count += 1
    for a in pubList:
            n.write(str(a).replace('u','').replace("'", '').replace('(', '').replace(')','').replace(",,", ','))
    n.write("\n+\n")
    pubSet = set(pubList)        
    dic[count] = pubSet
    pubList = []
    c1.execute("""SELECT latin_prefix FROM Organism""")
    organismList = []

    for row in c1:
        organismList.append(row[0])

    i=0
    pubList = []
    n.write(":")
    for i in organismList:
        statement1 = """SELECT  `Article_ID` 
        FROM  `Article-Organism` 
        WHERE Organism_prefix =  '"""+i+"""'"""
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
        count += 1
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
            if 1 == naam1 or 1 == naam2:
                totaal = len(set1 & set2)
                f.write(">" )
                f.write(str(y[0]))
                f.write("\n*")
                f.write(str(y[1]))
                f.write("\n#")
                f.write(str(set1 & set2).replace("set()", "").replace("u",'').replace("{","").replace("}","").replace("'","").replace("set(",'').replace(')','').replace("(","").replace("]","").replace("[",""))
                f.write("\n@")
                f.write(str(totaal))
                f.write("\n%\n")
  
    c1.close()
    f.close()
    n.close()

                
def organism(Substance):
    conn = mysql.connector.Connect(host='localhost',user='bi2_pg6',
                            password='blaat1234',database='InfiRap')

    c1 = conn.cursor()
    f=open("/home/bi2_pg6/public_html/Inficio Raptum/Python/edgesSearch.3j",'w')
    n=open("/home/bi2_pg6/public_html/Inficio Raptum/Python/nodesSearch.3j",'w')
    dic = {}
    i=0
    count = 0
    pubList = []
    c1.execute("""SELECT chemical_name FROM Compound""")
    compoundList = []
    for row in c1:
        compoundList.append(row[0])

    i=0
    pubList = []
    for i in compoundList:
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
        count += 1
        for a in pubList:
            n.write(str(a).replace('u','').replace("'", '').replace('(', '').replace(')','').replace(",,", ','))
        n.write("\n+\n")
        pubSet = set(pubList)        
        dic[count] = pubSet
        pubList = []
    statement1 = """SELECT  `Article_ID` 
    FROM  `Article-Organism` 
    WHERE Organism_prefix =  '"""+Substance+"""'"""
    c1.execute(statement1)
    n.write(":")
    for row in c1:
        pubList.append(row)
    n.write(">")
    n.write(str(count))
    n.write("\n*")
    n.write(str(Substance))
    n.write(" \n#")
    n.write(str(len(pubList)))
    n.write("\n@")
    count += 1
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
            if 1 == naam1 or 1 == naam2:
                totaal = len(set1 & set2)
                f.write(">" )
                f.write(str(y[0]))
                f.write("\n*")
                f.write(str(y[1]))
                f.write("\n#")
                f.write(str(set1 & set2).replace("set()", "").replace("u",'').replace("{","").replace("}","").replace("'","").replace("set(",'').replace(')','').replace("(","").replace("]","").replace("[",""))
                f.write("\n@")
                f.write(str(totaal))
                f.write("\n%\n")
  
    c1.close()
    f.close()
    n.close()
