from os import environ
import sys
from psycopg2 import connect
from uuid import uuid4

if len(sys.argv) < 4:
    print("Usage: python3 importDBColumn.py [fileName] [targetDBName] [targetTable]")
    exit(1)