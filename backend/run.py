import os
import sys

'''
if (not os.environ.get('SQLPassword')):
    print("Missing environment password for the PostgreSQL Account")
    exit(1)
elif (not os.environ.get('TAUCETI_SECRET_KEY')):
    print("Missing environment password for JWT Secret Key")
    exit(1)
'''

if len(sys.argv) < 4:
    print("Usage: python3 run.py [SQLPassword] [POINTR_SECRET_KEY] [SQLPassword] [init=False]")
    exit(1)

os.environ['POINTR_EMAIL_PASSWORD'] = sys.argv[1]
os.environ['POINTR_SERVER_SECRET'] = sys.argv[2]
os.environ['SQLPassword'] = sys.argv[3] 

from app import db, app

if __name__ == "__main__":
    db.create_all()

    from fillDB import addSoc, addEvent, addUser
    if len(sys.argv) == 5 and sys.argv[4].lower() == 'true':
        addSoc()
        addEvent()
        addUser()
        print("Database Initialised")
        exit(0)

    app.run(debug=True)