import os, sys
from time import sleep

docs = '''
Usage: python run.py <options>

args:
    dev: run in a dev environment
    init: initialise environment with mock data
'''

def initEnvironments():
    if not "POINTR_EMAIL_PASSWORD" in os.environ:
        os.environ['POINTR_EMAIL_PASSWORD'] =  input("POINTR_EMAIL_PASSWORD = ")
        print("Note: run ./login.sh to have a store env permanently")
    if not "POINTR_SERVER_SECRET" in os.environ:
        os.environ['POINTR_SERVER_SECRET'] =  input("POINTR_SERVER_SECRET = ")
        print("Note: run ./login.sh to have a store env permanently")
    if not "SQLPassword" in os.environ:
        os.environ['SQLPassword'] =  input("SQLPassword = ")
        print("Note: run ./login.sh to have a store env permanently")
def initDB():
    from databaseUtil.fillDB import addSoc, addEvent, addUser
    print("Initialising database.",end='', flush=True)
    for i in range(3):
        sleep(1)
        print(".",end='', flush=True)
    addSoc()
    addEvent()
    addUser()
    print("Database Initialised")
if __name__ == "__main__":
    print("Running...")
    print("Having issues due to updated db? run ./updateDB.sh")
    if "dev" in sys.argv:
        initEnvironments()
        print(os.environ)
        from app import db, app
        db.create_all()
        if "init" in sys.argv:
            initDB()
        print("Running app...")

        app.run(debug=True)
    else:
        print(docs)
