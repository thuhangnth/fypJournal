import MySQLdb as mysql
import numpy as np

#To create a table for a group of journals
def createTable(cursor, group):
    print '1'
    SQL_createTable = "CREATE TABLE %s (id)"
    cursor.execute(SQL_createTable, group)

def fillTable(cursor, group):
    SQL_fillTable = "INSERT INTO %s SELECT id, name, issn FROM journal WHERE name = %%s"  
    with open('OS.txt') as f:
        for line in f:
            name = line.rstrip()
            stmt = SQL_fillTable % group
            print stmt
            cursor.execute(stmt,(name))
            print line

def main():
    db = mysql.connect(
        host = "127.0.0.1",
        user = "root",
        passwd = "Masm@s91",
        db = "ranking",
        port = 3306)
    cursor = db.cursor()

    #createTable(cursor, "OS")
    fillTable(cursor, "os")

    db.commit()
    db.close()

if __name__ == "__main__":
    main()
