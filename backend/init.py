import os
# NOTE: Uncomment the five lines below when reinitialising the database is required
from util.events import createSingleEvent, createRecurrentEvent
from util.users import createUser
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
    createSingleEvent("z5161616", "1239", "Hackathon", "2019-11-19", True, findSocID("UNSW Hall"))
    createSingleEvent("z5333333", "0000", "Gamer Juice Winery Tour", "2019-09-09", True, findSocID("UNSW Hall"))
    createSingleEvent("z5555555", "1234", "Coffee Night", "2019-10-16", True, findSocID("UNSW Hall"))
    createSingleEvent("z5111111", "4231", "LoL Appreciation", "2019-09-08", True, findSocID("UNSW Hall"))

    # register users:
    #   for Hackathon
    register("z5161616", "1239", 'Steven')
    register("z5161798", "1239", 'Casey Neistat')
    #   for Gamer Juice Winery Tour
    register("z5333333", "0000", 'Ivan Velickovic')
    register("z5161798", "0000", 'Casey Neistat')
    register("z5161616", "0000", 'Stevn')
    #   for Coffee Night
    register("z5161616", "1234", 'Steven')
    register("z5161798", "1234", 'Casey Neistat')
    register("z5111111", "1234", 'Harrison Steyn')
    register("z5222222", "1234", 'Junyang Sim')
    register("z5333333", "1234", 'Ivan Velickovic')
    register("z5444444", "1234", 'Oltan Sevinc')
    register("z5555555", "1234", 'Will de Dassel')

def main():
    # os.system("rm database.db")
    
    initDatabase()

if __name__ == '__main__':
    main()