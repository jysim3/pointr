import os
from app import app
from flask_mail import Mail

if app.config['ENV'] == 'development':
    site = 'http://localhost:8000'
elif app.config['ENV'] == 'production':
    site = 'https://pointr.live'
# Utilising flask_mail
app.config.update(
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_PORT = 465,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = "shenthemaster@gmail.com",
    #MAIL_USERNAME = "pointr.help@gmail.com",
    MAIL_PASSWORD = os.environ.get("POINTR_EMAIL_PASSWORD")
)
mail = Mail(app)


def sendActivationEmail(stringToSend, emailToSend):
    message = f"""\
Hello,\nIt's good to have you with us. Thanks again for signing up with Pointr.\n\nHave fun accumulating your room points :).\n\nPlease activate your account now: {site}/{stringToSend}"""

    try:
        msg = mail.send_message(
            'Activate Your Pointr Account',
            sender=app.config['MAIL_USERNAME'],
            recipients=[f"{emailToSend}@student.unsw.edu.au"],
            body=message
        )
    except Exception:
        return str(Exception)
    return "success"


def sendForgotEmail(link, zID, emailToSend):
    message = f"""\
Hi,{zID}\nYou have requested to reset your password.\nFollow this link to reset your password: {site+link}"""

    try:
        msg = mail.send_message(
            'Reset Your Pointr Password',
            sender=app.config['MAIL_USERNAME'],
            recipients=[emailToSend],
            body=message
        )
    except Exception:
        return str(Exception)
    return "success"

def sendEnquiry(subject, message):
    recipients=["stevenshen1999@hotmail.com", "steynharrison1@gmail.com", "junyang.0607@gmail.com", "hello@ivanvelickovic.com"]
    #recipients=["stevenshen1999@hotmail.com", "shenthemaster@gmail.com"]

    try:
        msg = mail.send_message(
            subject,
            sender=app.config['MAIL_USERNAME'],
            recipients=recipients,
            body=message
        )
    except Exception:
        return str(Exception)
    return "success"

'''
def main():

    for i in range(0, 200):
        receiverEmail = f"z5{i:06d}@unsw.edu.au"
        sendActivationEmail("Yo wassup", receiverEmail)

        print(f"{receiverEmail} sent")

if __name__ == "__main__":
    main()
'''