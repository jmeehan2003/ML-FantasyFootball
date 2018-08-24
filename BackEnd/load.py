import csv, psycopg2

###########################################################################
# Author: Erid Durboraw
# File: load.py
# Purpose: No shit, it parses a csv file and loads it into the DB instance
# using psycopg2
###########################################################################

#Create db Connection
conn = psycopg2.connect(database="Cepheus_db",
                        user="db_usr",
                        password="B3av3rs1!",
                        host="osucepheus.cgwruhobay1w.us-east-2.rds.amazonaws.com",
                        port="5432")

#Create cursor with which to execute queries
cur = conn.cursor()

#Should you need a new table,uncomment and go with it. If you don't need it, grrrreat!

'''
tablename = 'tempdumptable' #you can name this whatever you want. You can name it Eric_ruined_christmas, just let me know so I can move the data
drop = 'DROP TABLE IF EXISTS ' + tablename
cur.execute(drop)
conn.commit()
ct = 'CREATE TABLE ' + tablename + ' (fname varchar(255), lname varchar(255), week int, yr int, actual int, predicted float);'
cur.execute(ct)
conn.commit()
'''

#parse csv
with open ('testOutput.csv') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',')
    for row in reader:
        #build query string
        query1 = 'INSERT INTO Results(fname, lname, week, yr, actual, predicted) VALUES '
        query2 =row['fname'], row['lname'], row['week'], row['yr'], row['actual'], row['predicted']
        query = str(query1) + str(query2)
        print(query)
        #execute query
        cur.execute(query)
#commit change
conn.commit()