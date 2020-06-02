from os import environ
import sys
from psycopg2 import connect
from uuid import uuid4

if len(sys.argv) < 3:
    print("Usage: python3 addSoc.py [socName] [socDescrition] [socType=0]")
    exit(1)

socName = sys.argv[1]
socDescription = sys.argv[2]
socType = 0 if len(sys.argv) == 3 else sys.argv[3]

conn = connect(database="pointrDB")
curs = conn.cursor()

try:
    curs.execute("INSERT INTO SOCIETIES(id, description, name, type) VALUES ((%s), (%s), (%s), (%s));",
        (uuid4().hex, socDescription, socName, socType,))
except Exception as e:
    print(e)
    exit(1)

conn.commit()
conn.close()