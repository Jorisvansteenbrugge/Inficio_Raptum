import mysql.connector
import json

conn = mysql.connector.Connect(host='localhost',user='bi2_pg6', password='blaat1234',database='InfiRap')
c1 = conn.cursor()
jSONData=[]#uiteindelijke output array die naar .JSON wordt geschreven


filepath = "/home/bi2_pg6/public_html/Joris's hideous testplace/nodes.3j" #bestandsnaam van de output
filepath2="/home/bi2_pg6/public_html/Joris's hideous testplace/edges.3j"

bestand = open(filepath,'w')
edges = open(filepath2,"w")


c1.execute("""SELECT DISTINCT  `Article_ID` ,  `Compound_Sysname` 
FROM  `Compound-Article` ,  `Compound` 
WHERE  `Compound_Sysname` =  `chemical_name` """)#chemische naam van coumpounds

compDic={}
for row in c1:# loopt over de chemische namen van de coumpounds
    #naam die nodig is voor de graph, "compound" is de clustering
    naam=row[1]
    if naam in compDic.keys():
        compDic[naam].add(row[0])
    else:
        compDic[naam]=set()
        compDic[naam].add(row[0])
        jSONData.append({"name":naam,"size":3000,"imports":[]}) 
        
     
c1.execute("""SELECT DISTINCT  `Article_ID` ,  `latin_prefix` ,  `latin_surname` 
FROM  `Article-Organism` ,  `Organism` 
WHERE  `Organism_surname` =  `latin_surname` """)


orgDic = {}
for row in c1:
    naam=row[1]+" "
    naam+=row[2]
    
    if naam in orgDic.keys():
        orgDic[naam].add(row[0])
    else:
        orgDic[naam]=set()
        orgDic[naam].add(row[0])

for waarde in orgDic.keys():
    #bestand.write("naam :  "+waarde)
    #bestand.write("\n\n")
    imports = []
    set1=orgDic[waarde]
    for value in compDic.keys():
        set2=compDic[value]
        lengte = len(set1&set2)
        if lengte!=0:
            imports.append(value)
            
    jSONData.append({"name":waarde,"size":3000,"imports":imports}) 


bestand.write('hahahaha')


#bestand.write(json.dumps(jSONData,indent=4))    
bestand.close()
edges.close()

