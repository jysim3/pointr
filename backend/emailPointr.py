import smtplib, ssl

def sendActivationEmail(stringToSend, emailToSend):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "pointr.help@gmail.com"
    receiver_email = emailToSend
    password = "!4wKrKwAp&WfU"
    message = f"""\
Subject: Activate Your Pointr Account

Hello,\nIt's good to have you with us. Thanks again for signing up with Pointr.\n\nPlease activate your account now: {stringToSend}"""

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)