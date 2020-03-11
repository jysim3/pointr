import datetime
#import pytz
#from util.utilFunctions import makeConnection
from util.utilFunctions import createConnection
from dateutil import tz

fromZone = tz.gettz('UTC')
toZone = tz.gettz('Australia/Sydney')

conn = createConnection()
curs = conn.cursor()
curs.execute("SELECT time, zid FROM participation;")
results = curs.fetchall()
for i in results:
    time = i[0].replace(tzinfo=fromZone)
    convertion = time.astimezone(toZone)
    curs.execute("UPDATE PARTICIPATION SET TIME = (%s) WHERE ZID = (%s);", (convertion, i[1],))

conn.commit()
