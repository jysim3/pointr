from os import environ
import sys
from psycopg2 import connect
from uuid import uuid4

conn = connect(database="pointrDB")
curs = conn.cursor()

with open("dumpPointrdbUsers.csv", "r") as file:
    file.readline() # Discarding header

    while(True):
        student = file.readline()
        if not student: break

        student = student.strip()
        listify = student.split(',')

        curs.execute('SELECT * FROM users WHERE "zID" = (%s);', (listify[0],))
        if curs.fetchone():
            continue

        curs.execute('''
        INSERT INTO users ("zID", password, "firstName", "lastName", "isArc", "commencementYear", "superadmin", activated)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);''',
        (listify[0], listify[3], listify[1], listify[2], listify[4], listify[5], listify[-3], listify[-2], ))

conn.commit()

print("Imported")