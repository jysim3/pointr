from os import environ
import sys
from psycopg2 import connect
from uuid import uuid4

if len(sys.argv) < 3:
    print("Usage: python3 migrateDB.py [dbName] [tableName] [dumpFile='dump{dbName}{tableName}.csv']")
    exit(1)

dbName = sys.argv[1]
tableName = sys.argv[2]
fileName = sys.argv[3] if len(sys.argv) > 3 else None

conn = connect(database=dbName)
curs = conn.cursor()

try:
    curs.execute(f"SELECT * FROM {tableName};")
except Exception as e:
    print(e)
    exit(1)

titles = [desc[0] for desc in curs.description]

results = curs.fetchall()

with open(fileName if fileName else f"dump{dbName.capitalize()}{tableName.capitalize()}.csv", "w") as file:
    file.write(f"{','.join(titles)}\n")

    for result in results:
        result = [str(i) for i in result]
        file.write(f"{','.join(result)}\n")

print(f"Finished dumping data, dumpfile name: dump{dbName.capitalize()}{tableName.capitalize()}.csv")