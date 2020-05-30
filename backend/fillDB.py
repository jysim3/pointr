from models.event import Event
from models.society import Societies
from models.user import Users
from uuid import uuid4
import random
from models.event import db
from string import ascii_uppercase, digits
from hashlib import sha256

socs = []

def addSoc():
    # Data Sanitation
    with open("mockDataNoDup.csv", "r") as file:
        for i in file:
            i = i.strip()
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
            result = Event(id=''.join(random.choices(ascii_uppercase + digits, k=5)), name=i[0], description=i[1],
            start=i[2], end=i[3], hasQR=True if i[4] == 'true' else False, 
            hasAccessCode=True if i[5] == 'true' else False,
            hasAdminSignin=True if i[6] == 'true' else False, 
            status=random.randint(0,2))
            result.hosting.append(socs[random.randint(0, 74)])
            db.session.add(result)

    db.session.commit()
    print("Added 300 random events")

def addUser():
    with open("mockUsersNoDup.csv", "r") as file:
        for i in file:
            i = i.strip()
            i = i.split(',')
            user = Users(zID=f"z{''.join(random.choices(digits, k=7))}",
            #password=sha256(''.join(random.choices(ascii_uppercase + digits, k=8)).encode()).hexdigest(),
            password=sha256('00000000'.encode()).hexdigest(),
            firstName=i[0], lastName=i[1], isArc=True if i[2] == 'true' else False, superadmin=False, activated=True)
            db.session.add(user)

    db.session.commit()
    print("Added in 1000 users")

def removeDuplicates(inputName, outputName):
    with open(inputName, "r") as inFile, open(outputName, "w") as outFIle:
        seen = {}
        for line in inFile:
            lineSplit = line.split(',')
            if lineSplit[0] in seen: continue
            seen[lineSplit[0]] = True
            outFIle.write(line)