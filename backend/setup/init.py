import os
import sys
sys.path.append('../')
# NOTE: Uncomment the five lines below when reinitialising the database is required
from util.events import createSingleEvent, createRecurrentEvent
from util.users import createUser, getUserAttendance
from util.participation import register
from util.societies import createSociety, createSocStaff, findSocID
from util.utilFunctions import checkEvent

def initDatabase():
    # Moving this section to init.py in the next patch lmao
    # add users
    createUser("z5161616", "Steven Shen", "123456")
    createUser("z5161798", "Casey Neistat", "123456")
    createUser("z5111111", "Harrison Steyn", "123456")
    createUser("z5222222", "JunYang Sim", "123456")
    createUser("z5333333", "Ivan Velickovic", "123456")
    createUser("z5444444", "Oltan Sevinc", "123456")
    createUser("z5555555", "Will de Dassel", "123456")

    createSociety("z5111111", "CSESoc")
    createSociety("z5161616", "Manchester United FC")
    createSociety("z5555555", "UNSW Hall")

    # NOTE: Defaults to UNSW Hall (for the society field right now)
    createSingleEvent("z5161616", "1239", "Hackathon", "2020-11-19", True, findSocID("UNSW Hall"))
    createSingleEvent("z5333333", "0000", "Gamer Juice Winery Tour", "2020-09-09", True, findSocID("UNSW Hall"))
    createSingleEvent("z5555555", "1234", "Coffee Night", "2020-10-16", True, findSocID("UNSW Hall"))
    createSingleEvent("z5111111", "4231", "LoL Appreciation", "2020-09-08", True, findSocID("UNSW Hall"))

    # register users:
    #   for Hackathon
    register("z5161616", "1239")
    register("z5161798", "1239")
    #   for Gamer Juice Winery Tour
    register("z5333333", "0000")
    register("z5161798", "0000")
    register("z5161616", "0000")
    #   for Coffee Night
    register("z5161616", "1234")
    register("z5161798", "1234")
    register("z5111111", "1234")
    register("z5222222", "1234")
    register("z5333333", "1234")
    register("z5444444", "1234")
    register("z5555555", "1234")

def main():
    # os.system("rm database.db")
    
    initDatabase()
    #print(getUserAttendance("z5161616"))

if __name__ == '__main__':
    main()