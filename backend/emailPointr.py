import smtplib, ssl
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
password = getPassword()
# FIXME: Move this line below into the database then delete it
#password = "!4wKrKwAp&WfU"
context = ssl.create_default_context()
server = smtplib.SMTP_SSL(smtp_server, port, context=context)
server.login(sender_email, password)

def sendActivationEmail(stringToSend, emailToSend):
    receiver_email = emailToSend
    message = f"""\
Subject: Activate Your Pointr Account

Hello,\nIt's good to have you with us. Thanks again for signing up with Pointr.\n\nPlease activate your account now: {stringToSend}"""

    server.sendmail(sender_email, receiver_email, message)