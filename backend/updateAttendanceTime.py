#import pytz
#from util.utilFunctions import makeConnection
from util.utilFunctions import createConnection
#from dateutil import tz
from datetime import timedelta, datetime

conn = createConnection()
curs = conn.cursor()
curs.execute("SELECT time, zid FROM participation;")
results = curs.fetchall()
for i in results:
    time = i[0] + timedelta(hours=11)
    curs.execute("UPDATE PARTICIPATION SET TIME = (%s) WHERE ZID = (%s);", (time, i[1],))

conn.commit()
