import os
import sys
sys.path.append('../')
from util.events import createSingleEvent, createRecurrentEvent
from util.users import createUser, getUserAttendance
from util.participation import register
from util.societies import createSociety, createSocStaff, findSocID, joinSoc
from util.utilFunctions import checkEvent
from datetime import datetime

def initDatabase():
    # Moving this section to init.py in the next patch lmao
    # add users
    #createUser("z5161616", "Steven Shen", "123456")
    createUser("z5161631", "Junyang Sim", "123456")
    createUser("z5111111", "Wayne Rooney", "123456")
    createUser("z5222222", "Ivan", "123456")
    createUser("z5333333", "Harrison", "123456")
    createUser("z5444444", "Memer", "123456")
    createUser("z5555555", "Oltan", "123456")
    #createUser("z5161616", "Da Captain", "123123")

    createSociety("z5111111", "CSESoc")
    createSociety("z5161631", "Manchester United FC")
    createSociety("z5222222", "UNSW Hall")
    createSociety("z5444444", "Exotic Beer Society")

    # NOTE: Defaults to UNSW Hall (for the society field right now)
    createSingleEvent("z5161631", "1239", "Hackathon", "2020-11-19", True, findSocID("CSESoc"), None, None)
    createSingleEvent("z5333333", "0000", "Gamer Juice Winery Tour", "2020-09-09", True, findSocID("UNSW Hall"), None, None, datetime.strptime("23:30:00", "%H:%M:%S"))
    createSingleEvent("z5222222", "KSJAM", "Test Event", "2020-02-23", False, findSocID("UNSW Hall"), None, None)
    createSingleEvent("z5111111", "1234", "LoL Appreciation", "2020-09-08", True, findSocID("UNSW Hall"))

    createRecurrentEvent("z5161616", "ASDZX", "Coffee Night", "2020-02-26", "2021-01-01", 7, "day", False, "UNSW Hall", findSocID("UNSW Hall"), "Weekly Wednesday gathering for UNSW Hall")

    # register users:
    #   for Hackathon
    joinSoc("z5161631", findSocID("CSESoc"))
    register("z5161631", "1239")
    joinSoc("z5222222", findSocID("CSESoc"))
    register("z5222222", "1239")
    #   for Gamer Juice Winery Tour
    register("z5333333", "0000")
    register("z5555555", "0000")
    register("z5161631", "0000")
    #   for Coffee Night
    register("z5161631", "1234")
    register("z5111111", "1234")
    register("z5222222", "1234")
    register("z5333333", "1234")
    register("z5444444", "1234")
    register("z5555555", "1234")

def main():
    # os.system("rm database.db")
    
    initDatabase()
    #print(getUserAttendance("z5161631"))

if __name__ == '__main__':
    main()