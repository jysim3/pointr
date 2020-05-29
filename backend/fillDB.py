from models.event import Event
from models.society import Societies
from uuid import uuid4
import random
from models.event import db

socs = []

def addSoc():
    # Data Sanitation
    with open("mockDataNoDup.csv", "r") as file:
        for i in file:
            i = i.split(',')
            results = Societies(id=uuid4().hex, description=i[1], name=i[0],
            type=random.randint(0, 8))
            socs.append(results)
            db.session.add(results)

    db.session.commit()
    print("Added 75 random societies")

def addEvent():
    #removeDuplicates("MOCK_DATA.csv", "mockEventsNoDup.csv")
    with open("mockEventsNoDup.csv", "r") as file:
        for i in file:
            i = i.strip()
            i = i.split(',')
            result = Event(id=str(uuid4().hex).upper()[:5], name=i[0], description=i[1],
            start=i[2], end=i[3], hasQR=True if i[4] == 'true' else False, 
            hasAccessCode=True if i[5] == 'true' else False,
            hasAdminSignin=True if i[6] == 'true' else False, 
            status=random.randint(0,2))
            result.hosting.append(socs[random.randint(0, 74)])
            db.session.add(result)

    db.session.commit()
    print("Added 300 random events")

def removeDuplicates(inputName, outputName):
    with open(inputName, "r") as inFile, open(outputName, "w") as outFIle:
        seen = {}
        for line in inFile:
            lineSplit = line.split(',')
            if lineSplit[0] in seen: continue
            seen[lineSplit[0]] = True
            outFIle.write(line)