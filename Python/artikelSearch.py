from Bio import Entrez
from Bio import Medline
import itertools
import sys



def main(Substance, Organism, Gene):
    zoekterm1 = "Cocaine"
    zoekterm2 = "Elegans"
    MAX_COUNT = 50
    dic = {}
    titels = []
    TERM = ''
    TERMS = []
    count = 1
    if zoekterm2 == "":
        TERM = zoekterm1
    if zoekterm1 == "":
        print("vul een zoekterm in")
        sys.exit()
    elif zoekterm2 != "":
        TERM = zoekterm1+" and "+zoekterm2
    TERMS.append(TERM)
    print(TERM)
    handle = Entrez.esearch(db="pubmed", term= TERM, retmax=MAX_COUNT)
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
    dic[TERM] = pubSet
    print(dic)
    return "Jay"

main(Substance, Organism, Gene)


