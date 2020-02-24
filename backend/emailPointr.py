import smtplib, ssl
import os
import sys
from util.utilFunctions import createConnection

def getPassword():
    conn = createConnection()
    curs = conn.cursor()
    curs.execute("SELECT * FROM encrypt;")
    results = curs.fetchall()
    return results[0][0]

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "pointr.help@gmail.com"
<<<<<<< HEAD

if (os.environ.get('POINTR_EMAIL_PASSWORD') == None):
    print("Missing environment secret key for email address. Set env variable POINT_EMAIL_PASSWORD to the password.")
    sys.exit()

password = os.environ.get('POINTR_EMAIL_PASSWORD')
=======
#password = getPassword()
# FIXME: Move this line below into the database then delete it
password = "!4wKrKwAp&WfU"
>>>>>>> f1a6fed9b96e0d2064b9787e0d523aa7062acb2b
context = ssl.create_default_context()
server = smtplib.SMTP_SSL(smtp_server, port, context=context)
server.login(sender_email, password)

def sendActivationEmail(stringToSend, emailToSend):
    receiver_email = emailToSend
    message = f"""\
Subject: Activate Your Pointr Account

Hello,\nIt's good to have you with us. Thanks again for signing up with Pointr.\n\nPlease activate your account now: {stringToSend}"""

    server.sendmail(sender_email, receiver_email, message)