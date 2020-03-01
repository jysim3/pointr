import os
import sys
sys.path.append('../')
from util.events import createSingleEvent, createRecurrentEvent
from util.users import createUser, getUserAttendance, activateAccount
from util.participation import register
from util.societies import createSociety, createSocStaff, findSocID, joinSoc, makeSuperAdmin
from util.utilFunctions import checkEvent
from datetime import datetime
import uuid

def generateID(number = None):
    return str(uuid.uuid4().hex).upper()[:5]

def initDatabase():
    # Moving this section to init.py in the next patch lmao
    # add users
    createUser("z5161631", "Junyang Sim", "12345678")
    activateAccount("z5161631")
    createUser("z5111111", "Wayne Rooney", "12345678")
    activateAccount("z5111111")
    createUser("z5222222", "Ivan", "12345678")
    activateAccount("z5222222")
    createUser("z5333333", "Harrison", "12345678")
    activateAccount("z5333333")
    createUser("z5444444", "Memer", "12345678")
    activateAccount("z5444444")
    createUser("z5555555", "Oltan", "12345678")
    activateAccount("z5555555")
    createUser("z5000000", "Super Admin Test Account", "gangboss", isSuperAdmin=True)
    activateAccount("z5000000")

    # TODO: FIXME: When creating societies, add in any existing superAdmins into the newly created socs
    createSociety("z5111111", "CSESoc")
    createSociety("z5161631", "Manchester United FC")
    createSociety("z5222222", "UNSW Hall")
    createSociety("z5444444", "Exotic Beer Society")

    createUser("z5111000", "Test Superadmin 2", "12345678", isSuperAdmin=True)
    activateAccount("z5111000")

    # NOTE: Defaults to UNSW Hall (for the society field right now)
    event1 = createSingleEvent("z5111111", generateID(), "Hackathon", "2020-11-19", True, findSocID("CSESoc"), None, None)
    event2 = createSingleEvent("z5161631", generateID(), "Gamer Juice Winery Tour", "2020-09-09", True, findSocID("Manchester United FC"), None, None, None, datetime.strptime("23:30:00", "%H:%M:%S"))
    event3 = createSingleEvent("z5222222", generateID(), "Test Event", "2020-02-23", False, findSocID("UNSW Hall"), None, None)
    event4 = createSingleEvent("z5444444", generateID(), "LoL Appreciation", "2020-09-08", True, findSocID("Exotic Beer Society"))
    event5 = createSingleEvent("z5222222", generateID(), "Assassin's week", "2020-03-01", True, findSocID("UNSW Hall"), "UNSW Hall", None, "12:30", "20:30")

    event5 = createRecurrentEvent("z5222222", generateID(), "Coffee Night", "2020-02-26", "2021-01-01", 7, "day", False, "UNSW Hall", findSocID("UNSW Hall"), "Weekly Wednesday gathering for UNSW Hall")

    # register users:
    #   for Hackathon
    joinSoc("z5161631", findSocID("CSESoc"))
    register("z5161631", event1[0])
    joinSoc("z5222222", findSocID("CSESoc"))
    register("z5222222", event1[0])
    #   for Gamer Juice Winery Tour
    joinSoc("z5333333", findSocID("Manchester United FC"))
    register("z5333333", event2[0])
    joinSoc("z5555555", findSocID("Manchester United FC"))
    register("z5555555", event2[0])
    register("z5161631", event2[0])
    #   for Coffee Night
    joinSoc("z5161631", findSocID("UNSW Hall"))
    register("z5161631", event3[0])
    joinSoc("z5111111", findSocID("UNSW Hall"))
    register("z5111111", event3[0])
    joinSoc("z5222222", findSocID("UNSW Hall"))
    register("z5222222", event3[0])
    joinSoc("z5333333", findSocID("UNSW Hall"))
    register("z5333333", event3[0])
    joinSoc("z5444444", findSocID("UNSW Hall"))
    register("z5444444", event3[0])
    joinSoc("z5555555", findSocID("UNSW Hall"))
    register("z5555555", event3[0])

def main():
    initDatabase()

if __name__ == '__main__':
    main()