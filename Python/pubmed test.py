from Bio import Entrez
from Bio import Medline
import itertools


 
MAX_COUNT = 50



bestand = open("terms.txt")
f = open('edges.3j', 'w')
n = open('nodes.3j', 'w')
dic = {}
titels = []
TERM = ''
TERMS = []
count = 1
for regel in bestand:
    TERM =regel.replace('\n', '')
    TERMS.append(TERM)
    print(TERM)
    handle = Entrez.esearch(db="pubmed", term= regel, retmax=MAX_COUNT)
    record = Entrez.read(handle)
    idlist = record["IdList"]
    handle = Entrez.efetch(db="pubmed", id=idlist, rettype="medline",
                               retmode="text")
    records = Medline.parse(handle)
    records = list(records)
    for record in records:
        titel = record.get("PMID","?")
        titels.append(titel)
        pubSet = set(titels)        
    dic[count] = pubSet
    n.write(">")
    n.write(str(count))
    n.write("\n*")
    n.write(str(TERM))
    n.write(" \n#")
    n.write(str(len(pubSet)))
    n.write("\n@\n")
    titels = []
    count+=1
n.close()
total = len(TERMS)
vergelijk = list(itertools.combinations(dic.values(), 2))
vergelijknamen = list(itertools.combinations(dic.keys(), 2))
for (i, a) in zip(vergelijk, vergelijknamen):
        set1 = i[0]
        naam1 = a[0]
        set2 = i[1]
        naam2 = a[1]
        totaal = len(set1 & set2)
        f.write(">" )
        f.write(str(a[0]))
        f.write("\n*")
        f.write(str(a[1]))
        f.write("\n#")
        f.write(str(set1 & set2).replace("set()", "").replace("{","").replace("}","").replace("'",""))
        f.write("\n@")
        f.write(str(totaal))
        f.write("\n%\n")
f.close()


