import urllib2
from bs4 import BeautifulSoup
import re
import MySQLdb as mysql

SQL_updateTolDoc = "UPDATE totaldocuments SET %s = %%s where issn =%%s"
def main():
    db = mysql.connect(
        host = "127.0.0.1",
        user = "root",
        passwd = "Masm@s91",
        db = "ranking",
        port = 3306)
    cursor = db.cursor()
    limit = 500
    offset = 500*23
    SQL_getIssn = "SELECT issn from totaldocuments LIMIT %s OFFSET %s"
    issnList = []
    notFound = []
    cursor.execute(SQL_getIssn,(limit,offset))
    rows = cursor.fetchall()
    for row in rows:
        (data,) = row
        issnList.append(data)
    for i in range(len(issnList)):
        #print issnList[i]
        articleNo = getArtNo(issnList[i])
        if articleNo != None:
            for j in range(len(articleNo)):
                year = 1999+j
                if articleNo[j] != "-":
                    yearStr = "`" + str(year) + "`"
                    stmt = SQL_updateTolDoc % yearStr
                    #print stmt
                    articleNo[j] = articleNo[j].replace('.','')
                    cursor.execute(stmt,(articleNo[j], issnList[i]))
            db.commit()
        else:
            notFound.append(issnList[i])
    db.close()
    print len(notFound)
    print notFound
def getArtNo(issn):
    url = 'http://www.scimagojr.com/journalsearch.php?q=' + issn + '&tip=iss'
    page = urllib2.urlopen(url)
    html_doc = page.read()
    soup = BeautifulSoup(html_doc, "html5lib")
    table = soup.find(class_=re.compile("par"))
    if (table!=None):
        articleNo = table.find_all(string = True)
        articleNo = articleNo[1:]
        for i in range(len(articleNo)):
            articleNo[i] = articleNo[i].encode('ascii')
        #print articleNo
        return articleNo
    else:
        #print table
        return None
if __name__ == "__main__":
    main()
