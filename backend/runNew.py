import os
import sys

'''
if (not os.environ.get('SQLPassword')):
    print("Missing environment password for the PostgreSQL Account")
    exit(1)
elif (not os.environ.get('TAUCETI_SECRET_KEY')):
    print("Missing environment password for JWT Secret Key")
    exit(1)
if len(sys.argv) < 4:
    print("Usage: python3 run.py [SQLPassword] [POINTR_SECRET_KEY] [SQLPassword]")
    exit(1)
'''

if not os.environ.get('POINTR_EMAIL_PASSWORD'):
    print("POINTR_EMAIL_PASSWORD not set up, run ./login.sh")
    exit(1)

if not os.environ.get('POINTR_SERVER_SECRET'):
    print("POINTR_SERVER_SECRET not set up, run ./login.sh")
    exit(1)

if not os.environ.get('SQLPassword'):
    print("SQLPassword not set up, run ./login.sh")
    exit(1)

from app import db, app

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
