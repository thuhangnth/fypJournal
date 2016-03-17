import urllib2
from bs4 import BeautifulSoup
import re
import MySQLdb as mysql

def main():
    db = mysql.connect(
        host = "127.0.0.1",
        user = "root",
        passwd = "Masm@s91",
        db = "ranking",
        port = 3306)
    cursor = db.cursor()
    SQL_getIssn = "SELECT issn from natureindex_score"
    SQL_updateIF = "UPDATE natureindex_score SET sjr_2014 =%s where issn=%s"

    issnList = []
    cursor.execute(SQL_getIssn)
    rows = cursor.fetchall()
    for row in rows:
        (data,) = row
        issnList.append(data)

    for i in range(len(issnList)):
        score = getSJR(issnList[i])
        if score != None:
            score = score.replace(',','.')
            cursor.execute(SQL_updateIF,(score, issnList[i]))
    db.commit()

def getIF(issn):
    url = 'http://www.scimagojr.com/journalsearch.php?q=' + issn + '&tip=iss'
    page = urllib2.urlopen(url)
    html_doc = page.read()
    soup = BeautifulSoup(html_doc, "html5lib")
    table = soup.find_all(class_="tabla_datos")
    if len(table)>1:
        rows = table[1].find_all("tr")
        data = rows[10].find_all(string = True)
        data[-1] = data[-1].encode('ascii')
        print data[-1]
        return data[-1]
    else:
        return None

def getSJR(issn):
    url = 'http://www.scimagojr.com/journalsearch.php?q=' + issn + '&tip=iss'
    page = urllib2.urlopen(url)
    html_doc = page.read()
    soup = BeautifulSoup(html_doc, "html5lib")
    table = soup.find_all(class_="tabla_datos")
    if len(table)>1:
        rows = table[1].find_all("tr")
        data = rows[1].find_all(string = True)
        data[-1] = data[-1].encode('ascii')
        print data[-1]
        return data[-1]
    else:
        return None

if __name__ == "__main__":
    main()
