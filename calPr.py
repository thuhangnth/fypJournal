import MySQLdb as mysql
import numpy as np
from ast import literal_eval
import time
import math

def getCoreSet(cursor,group):
    SQL_selectID = "SELECT id from %s"
    coreSet = []
    group = "`" + group + "`"
    stmt = SQL_selectID % group
    cursor.execute(stmt)
    for row in cursor:
        (data,) = row
        coreSet.append(data)
    return coreSet
    
def updateMatrix(matrixCite, citingID, citedID, noCite, idToIndex, indexToId, i):
    if idToIndex.has_key(citingID):
    	col = idToIndex[citingID]
    else:
    	idToIndex[citingID] = i
    	col = i
    	indexToId[i] = citingID
    	i = i+1
				
    if idToIndex.has_key(citedID):
    	row = idToIndex[citedID]
    else:
        idToIndex[citedID] = i
        row = i
        indexToId[i] = citedID
        i = i+1
		
    return i , row, col

def getP(matrixCite, size, idToIndex):
    totalCiting = np.sum(matrixCite, axis=0) #axis=0 means vertical sum
    matrixCite /= totalCiting

def calPR(pMatrix, prMatrix):
    while(True):
        pr = np.dot(pMatrix, prMatrix)
        if(np.allclose(pr,prMatrix,rtol=0)):
           return pr
        prMatrix = pr
    
def main():
    db = mysql.connect(
        host = "127.0.0.1",
        user = "root",
        passwd = "Masm@s91",
        db = "ranking",
        port = 3306)
    cursor = db.cursor()

    selfWeight = 1
    coreSet = getCoreSet(cursor, 'natureindex')
    n = len(coreSet)
    matrixCite = np.zeros([n,n])

    idToIndex = {}
    indexToId = {}
    i=0

    limit = 1000000
    offset = 0
    SQL_getCitation = "SELECT citingJournalId, citedJournalId, num from citation where DATE(citingTime) = '2010-01-01' AND DATE(citedTime) >= '2007-01-01' AND DATE(citedTime) < '2010-01-01' LIMIT %s OFFSET %s "
    cursor.execute(SQL_getCitation,(limit, offset))
    rows = cursor.fetchall()
    while len(rows)>0:
        for row in rows:
            (citingJournal, citedJournal, num) = row
            if ((citingJournal in coreSet) and (citedJournal in coreSet)):
                i, indexRow, indexCol = updateMatrix(matrixCite, citingJournal, citedJournal, num, idToIndex, indexToId, i)
                if (indexRow != indexCol):
                    matrixCite[indexRow, indexCol] += num
        offset += limit
        cursor.execute(SQL_getCitation, (limit, offset))
        rows = cursor.fetchall()
    print "Done fetching data"
    getP(matrixCite,i,idToIndex)
    matrixCite[np.isnan(matrixCite)]=0

    initPR = np.ones([n,1])
    initPR = initPR*1.0/n
    initPR = np.matrix(initPR)
    matrixCite = np.matrix(matrixCite)
    pr = calPR(matrixCite, initPR)

    print pr

    SQL_updatePR = "UPDATE natureindex_3y SET PR2010_E0S0 = %s where id = %s"
    for key in indexToId:
        cursor.execute(SQL_updatePR,(float(pr[key]),indexToId[key]))
    db.commit()
    db.close()

if __name__ == "__main__":
    main()
