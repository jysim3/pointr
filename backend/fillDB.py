from util.users import createUser
from util.societies import createSociety
from util.events import createSingleEvent
from util.utilFunctions import makeConnection
from uuid import uuid4
import random

socIDs = []

def addSoc():
    # Data Sanitation
    '''
    with open("MOCK_DATA.csv", "r") as inFile, open("mockDataNoDup.csv", "w") as outFIle:
        seen = {}
        for line in inFile:
            lineSplit = line.split(',')
            if lineSplit[0] in seen: continue
            seen[lineSplit[0]] = True
            outFIle.write(line)
    '''
    with open("mockDataNoDup.csv", "r") as file:
        for i in file:
            i = i.split(',')
            results = createSociety("z5161616", i[0], False, None, i[1])
            print(f"SocName: {i[0]}, SocDescription: {i[1]}, socID:{results}")
            socIDs.append(results)
    print("Added 75 random societies")

def addEvent():
    #removeDuplicates("MOCK_DATA.csv", "mockEventsNoDup.csv")
    with open("mockEventsNoDup.csv", "r") as file:
        for i in file:
            i = i.split(',')
            '''
            startTime = f"{i[-1][:-1]} {i[-3]}"
            endTime = f"{i[-1][:-1]} {i[-2]}"
            print(startTime, endTime)
            '''
            eventDate = i[-1][:-1]
            result = createSingleEvent("z5161616", str(uuid4().hex).upper()[:5], i[0], eventDate, 
            False, socIDs[random.randint(0, 74)], None, i[1], i[-3],
            i[-2], True, False)
            print(f"EventName: {i[0]}, EventID: {result[0]}")
    print("Added 200 random events")

def removeDuplicates(inputName, outputName):
    with open(inputName, "r") as inFile, open(outputName, "w") as outFIle:
        seen = {}
        for line in inFile:
            lineSplit = line.split(',')
            if lineSplit[0] in seen: continue
            seen[lineSplit[0]] = True
            outFIle.write(line)

if __name__ == "__main__":
    print("Reading Data From mockDataNoDup.csv.csv")
    addSoc()
    print("Reading Data From mockEventsNoDup.csv")
    addEvent()