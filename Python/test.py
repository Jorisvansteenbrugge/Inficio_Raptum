from Bio import Entrez
from Bio import Medline
import itertools
import mysql.connector

MAX_COUNT = 2
abstract = ""
title = ""
author= ""
date= ""
substance= ""
fout = ''
kaas = ''
dic = {}
pubmids = []
TERM = ''
count = 1
i = 0
a = '0'
db = mysql.connector.connect(host="localhost", # your host, usually localhost
                     user="bi2_pg6", # your username
                      passwd="blaat1234", # your password
                      db="InfiRap"# name of the data base
                       ,buffered=True) 
cur = db.cursor()
cur1 = db.cursor()


organismecheck = cur.execute("SELECT * FROM Organism")
artikelcheck = cur.execute("SELECT * FROM Article")
tussen1 = cur.execute("SELECT * FROM `Article-Author`")
tussen2 = cur.execute("SELECT * FROM `Article-Organism`")
tussen3 = cur.execute("SELECT * FROM `Compound-Article`")
auteurcheck = cur1.execute("SELECT * FROM Author")
anumm = cur1.rowcount +1
Organism = "Caenorhabditis.elegans"
Substance = "Zinc"
file = open("/home/bi2_pg6/public_html/Inficio Raptum/Python/dbarticle.txt",'w')


##if form.has_key('Substance'and'Organism'):
##    Substance = '%s' %form['Substance']
##    Organism = '%s'%form['Organism']
if Organism == "mineturtle":
        dic = 'HELLOOOOOO'


else:	
  TERM = Substance+" AND "+Organism
  handle = Entrez.esearch(db="pubmed", term= TERM, retmax=MAX_COUNT)
  record = Entrez.read(handle)
  idlist = record["IdList"]
  handle = Entrez.efetch(db="pubmed", id=idlist, rettype="medline",
  retmode="text")
  records = Medline.parse(handle)
  records = list(records)
  for record in records:
      abstract = ""
      title = ""
      author= ""
      date= ""
      substance= ""
      Split= ""
      prefix= ""
      surname= ""
      Abstract = record.get("AB","?")
      title = record.get("TI","?")
      author = ', '.join(record.get("AU","?"))
      date = record.get("DA","?")
      pubmedID = record.get("PMID","?")
      Split = Organism.split(".")
      prefix = Split[0]
      surname = Split[1]
      print prefix
      print surname

     
      if artikelcheck.index(str(pubmedID)) != -1:
          cur.execute('insert into Article (articleID, publication_date, article_title) values("%s", "%s", "%s")' % \
      (pubmedID, date, title))
      if auteurcheck.index(author) != -1:
          cur.execute('insert into Author (id, Name) values ("%d","%s")' % \
                      (anumm, author))
      if tussen1.index(str(anumm)) != -1:
          cur.execute('insert into `Article-Author`(Article_ID, Author_ID) values("%s", "%d")' % \
    (pubmedID, anumm))
      if organismecheck.index(Organism) != -1:
          cur.execute('insert into Organism(latin_surname, latin_prefix) values("%s", "%s")' % \
    (surname,prefix))
      if tussen2.index(str(pubmedID)) != -1:
          cur.execute('insert into `Article-Organism`(Article_ID, Organism_surname) values("%s","%s")' %\
                      (pubmedID, surname))
      if tussen3.index(str(pubmedID)) != -1:    
          cur.execute('instert into `Compound-Article`(Article_ID , Compound_Sysname) values("%s","%s")' %\
                      (pubmedID, Substance))
      if compoundcheck.index(Substance) != -1:
          cur.execute('insert into Compound(chemical_name) values("%s")' % \
    (Substance))
      


cur.close()
cur1.close()

db.commit()			
file.close()
db.close()		  

