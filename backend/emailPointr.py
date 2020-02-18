import smtplib, ssl

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "pointr.help@gmail.com"  # Enter your address
receiver_email = "stevenshen1999@hotmail.com"  # Enter receiver address
password = "!4wKrKwAp&WfU"
message = """\
Subject: Activate Your Pointr Account

Activation Link: This message is sent from Python."""

context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)