from util.events import getCurrentlyRunningEvents, updateAccessCode
from random import SystemRandom
import string

# Function designed to change the access codes for events
def tick():
    runningEvents = getCurrentlyRunningEvents()
    for i in runningEvents:
        currentAccessCode = ''.join(SystemRandom().choices(string.ascii_uppercase + string.digits, k=5))
        updateAccessCode(i, currentAccessCode)