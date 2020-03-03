import smtplib, ssl
import os
import sys
from util.utilFunctions import createConnection

if (os.environ.get('POINTR_EMAIL_PASSWORD') == None):
    print("Missing environment secret key for email address. Set env variable POINT_EMAIL_PASSWORD to the password.")
    sys.exit()

def sendActivationEmail(stringToSend, emailToSend):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "pointr.help@gmail.com"
    receiver_email = emailToSend
    password = os.environ.get('POINTR_EMAIL_PASSWORD')
    context = ssl.create_default_context()
    server = smtplib.SMTP_SSL(smtp_server, port, context=context)
    server.login(sender_email, password)

    message = f"""\
Subject: Activate Your Pointr Account

Hello,\nIt's good to have you with us. Thanks again for signing up with Pointr.\n\nHave fun accumulating your room points :).\n\nPlease activate your account now: {stringToSend}"""

    server.sendmail(sender_email, receiver_email, message)






def sendForgotEmail(link, zID, emailToSend):
    receiver_email = emailToSend
    message = f"""\
Subject: Password Reset Request 

Hi,{zID}\nYou have requested to reset your password.\nFollow this link to reset your password: {link}"""

    server.sendmail(sender_email, receiver_email, message)