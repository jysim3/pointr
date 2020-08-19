import sys
from util.societies import makeAdmin, findSocID
zID = sys.argv[1]

result = makeAdmin(zID, findSocID("UNSW Hall"))
print(result)
