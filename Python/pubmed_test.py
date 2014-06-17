import sys
sys.path.append('/home/bi2_pg6/public_html/Inficio Raptum/Python/')
from Bio import Entrez
from Bio import Medline
import MySQLdb as con
import logging


def __init__(self):
    logging.basicConfig(filename='/home/bi2_pg6/public_htmlInficio Raptum/Python/app.log',level=logging.DEBUG)
    #if form.has_key('Substance'and'Organism')
    #    TERM1 = '%s' %form['Substance']
    #    TERM2 = '%s'%form['Organism']
    #    TERMS = ('(' +TERM1 + ')' + 'AND'+ '('+TERM2 + ')')
    
    self.TERM1 = "2-Methoxyaniline"
    self.TERM2 = "Caenorhabditis elegans"
    self.TERMS = ('(' +self.TERM1 + ')' + 'AND'+ '('+self.TERM2 + ')')

    Entrez.email = "A.N.Other@example.com"     # Always tell NCBI who you are
    handle = Entrez.egquery(term=self.TERMS)
    record = Entrez.read(handle)
    for row in record["eGQueryResult"]:
        if row["DbName"]=="pubmed":
            print(row["Count"])
                     
    handle = Entrez.esearch(db="pubmed", term=self.TERMS, retmax=463)
    record = Entrez.read(handle)

    handle = Entrez.efetch(db="pubmed", id=record["IdList"], rettype="medline")
    records = Medline.parse(handle)
    records = list(records)

    self.title = []
    self.authors = []
    self.source = []
    self.abstract = []
    self.date = []
    self.pubmedID = []

    for record in records:
        self.title.append(record.get("TI", "?"))
        self.authors.append(record.get("AU", "?"))
        self.source.append(record.get("SO", "?"))
        self.abstract.append(record.get("AB", "?"))
        self.date.append(record.get("DA", "?"))
        self.pubmedID.append(record.get("PMID","?"))

 # Open database connection
    self.dataB=con.connect(host="localhost", # your host, usually localhost
    user="bi2_pg6", # your username
    passwd="blaat1234", # your password
    db="InfiRap") # name of the data base

# prepare a cursor object using cursor() method
    cursor1 = self.dataB.cursor()
    


    try:
    # Execute the SQL command
        cursor1.execute("SELECT chemical_name FROM `Compound` WHERE chemical_name = '"+self.TERM1+"'")
        substanceExists = cursor1.rowcount > 0
        cursor1.close()
        cursor2 = self.dataB.cursor()
        cursor2.execute("SELECT latin_surname FROM `Organism` WHERE latin_surname = '"+self.TERM2+"'")
        organismExists = cursor1.rowcount > 0
        cursor2.close()

        if not substanceExists:
            self.insertSubstance()
            self.dataB.commit()

    except con.Error, e:
            logging.debug(e)

    cursor1.close()
    self.dataB.close()

def insertSubstance(self):
        cursor = self.dataB.cursor()
        cursor.executemany("INSERT INTO `Compound`(chemical_name) VALUES ('"+self.TERM1+"')")
        cursor.close()


