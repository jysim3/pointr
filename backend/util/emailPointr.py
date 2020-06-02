import os
from app import app
from flask_mail import Mail, Message
from threading import Thread

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

def sendAsyncMail(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            print(e)
            return str(e)

def sendActivationEmail(stringToSend, emailToSend):
    message = Message('Activate Your Pointr Account', sender=app.config['MAIL_USERNAME'],
    recipients=[f"{emailToSend}@ad.unsw.edu.au"])
    message.body = f"""\
Hello,\nIt's good to have you with us. Thanks again for signing up with Pointr.\n\nActivate your account now: {site}/activate/{stringToSend}"""

    # Async version
    Thread(target=sendAsyncMail, args=(app, message)).start()
    #mail.send(message)
    return "success"


def sendForgotEmail(link, zID):
    message = Message('Reset Your Pointr Password', sender=app.config['MAIL_USERNAME'],
    recipients=[f"{zID}@ad.unsw.edu.au"])
    message.body = f"""\
Hi,{zID}\nYou have requested to reset your password.\nFollow this link to reset your password: {site}/reset/{link}"""

    # Async version
    Thread(target=sendAsyncMail, args=(app, message)).start()
    return "success"

def sendEnquiry(sender, content):
    recipients=["stevenshen1999@hotmail.com", "steynharrison1@gmail.com", "junyang.0607@gmail.com", "hello@ivanvelickovic.com"]
    #recipients=['stevenshen1999@hotmail.com']
    message = Message('Enquire Email For Pointr', sender=app.config['MAIL_USERNAME'],
    recipients=recipients)

    message.body = f"""
        Hello there,
        {sender} has send an enquiry about pointr:

        {content}

        Regards
    """

    # Async version
    Thread(target=sendAsyncMail, args=(app, message)).start()
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
