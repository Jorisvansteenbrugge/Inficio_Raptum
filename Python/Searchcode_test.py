import sys
sys.path.append('/home/bi2_pg6/public_html/Inficio Raptum/Python/')
from Bio import Entrez
from Bio import Medline
import MySQLdb as con

class Search():

    def __init__(self):
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
            cursor1.execute("SELECT chemical_name FROM Compounds WHERE chemical_name = '"+self.TERM1+"'")
            substanceExists = cursor1.rowcount > 0
            cursor1.close()
            cursor1 = self.dataB.cursor()
            cursor1.execute("SELECT latin_surname FROM organism WHERE latin_surname = '"+self.TERM2+"'")
            organismExists = cursor1.rowcount > 0
            cursor1.close()

            if not substanceExists and not organismExists:
                self.insertSubstance()
                self.insertOrganism()
                self.insertAuteur()
                self.insertTussen2()
                self.insertTussen3()
                self.insertArtikelen()
                self.dataB.commit()
            elif not substanceExists:
                self.insertSubstance()
                self.insertAuteur()
                self.insertTussen3()
                self.insertArtikelen()
                self.dataB.commit()
            elif not organismExists:
                self.insertOrganism()
                self.insertAuteur()
                self.insertTussen2()
                self.insertArtikelen()
                self.dataB.commit()
                
        
        except:
                   # Rollback in case there is any error
            self.dataB.rollback()
        # disconnect from server
        cursor1.close()
        self.dataB.close()

    def insertSubstance(self):
        cursor = self.dataB.cursor()
        cursor.execute("INSERT INTO Compound(chemical_name) VALUES ('"+self.TERM1+"')")
        cursor.close()

    def insertOrganism(self):
        cursor = self.dataB.cursor()
        Split = self.TERM2.split(" ")
        prefix = Split[0]
        surname = Split[1]
        cursor.execute('INSERT INTO Organism(latin_surname, latin_prefix) VALUES("%s", "%s")' % \
        (surname,prefix))
        cursor.close()

    def insertAuteur(self):
        cursor = self.dataB.cursor()
        i = 0
        while(i<len(self.title)):
             cursor.close()
             _authors = ','.join(self.authors[i]).replace("'","")
             cursor.execute("INSERT INTO Author(Name) VALUES ('"+_authors+"')")
             i+=1
        
##    def insertTussen1(self):
##        cursor = self.dataB.cursor()
##        cursor.execute("SELECT substance_id FROM substances WHERE substance = '"+self.TERM1+"'")
##        Term1ID = cursor.fetchone()[0]
##        cursor.execute('INSERT INTO `Article-Author`(Article_ID, Author_ID) values("%s", "%d")' % \
##            (pubmedID, anumm))
##        cursor.close()
##
    def insertTussen2(self):
        cursor = self.dataB.corsor()
        Split = self.TERM2.split(" ")
        surname = Split[1]
        i = 0
        while(i<len(self.title)):
             cursor.close()
             _pubmedID = self.pubmedID[i].replace("'","")
             command = 'INSERT INTO `Article-Organism`(Article_ID, Organism_surname) VALUES({0},{1})'.format("'"+_pubmedID+"'",surname)      
             cursor.execute(command)
             i+=1

    def insertTussen3(self):
        cursor = self.dataB.corsor()
        i = 0
        while(i<len(self.title)):
             cursor.close()
             _pubmedID = self.pubmedID[i].replace("'","")
             command = 'INSERT INTO `Compound-Article`(Article_ID, Compound_Sysname) VALUES({0},{1})'.format("'"+_pubmedID+"'", TERM1)      
             cursor.execute(command)
             i+=1
        
    def insertArtikelen(self):
        cursor = self.dataB.cursor()
        i=0
        while(i<len(self.title)):
            cursor.close()
            cursor = self.dataB.cursor()
            _title = self.title[i].replace("'","")
            magazine = self.source[i].replace("'","")
            _date = self.date[i].replace("'","")
            _abstract = self.abstract[i].replace("'","")
            _pubmedID = self.pubmedID[i].replace("'","")
            command = 'INSERT INTO Article (articleID, article_title, magazine, publication_date, abstract) VALUES ({0},{1},{2},{3},{4})'.format("'"+_pubmedID+"'", "'"+_title+"'", "'"+magazine+"'", "'"+_date+"'", "'"+_abstract+"'")
            cursor.execute(command)
            i+=1

def main():
    S = Search()

main()
    
    
