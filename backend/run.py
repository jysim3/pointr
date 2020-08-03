import os
import sys

# NOTE: No longer required
if len(sys.argv) < 4:
    print("Usage: python3 run.py [POINTR_EMAIL_PASSWORD] [POINTR_SECRET_KEY] [SQLPassword] [env=development] [init=False]")
    exit(1)

os.environ['POINTR_EMAIL_PASSWORD'] = sys.argv[1]
os.environ['POINTR_SERVER_SECRET'] = sys.argv[2]
os.environ['SQLPassword'] = sys.argv[3] 


from app import db, app

if __name__ == "__main__":
    db.create_all()

    from fillDB import addSoc, addEvent, addUser
    if len(sys.argv) >= 5:
        os.environ['FLASK_ENV'] = sys.argv[4] 
        print(sys.argv[4])
    if len(sys.argv) >= 6 and sys.argv[5].lower() == 'true':
        addSoc()
        addEvent()
        addUser()
        print("Database Initialised")
        exit(0)

    app.run(debug=True)
