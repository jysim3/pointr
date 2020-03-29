import os
from app import app
from flask_mail import Mail

# Utilising flask_mail
app.config.update(
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_PORT = 465,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = "pointr.help@gmail.com",
    MAIL_PASSWORD = os.environ.get("POINTR_EMAIL_PASSWORD")
)
mail = Mail(app)


def sendActivationEmail(stringToSend, emailToSend):
    message = f"""\
Hello,\nIt's good to have you with us. Thanks again for signing up with Pointr.\n\nHave fun accumulating your room points :).\n\nPlease activate your account now: {stringToSend}"""

    try:
        msg = mail.send_message(
            'Activate Your Pointr Account',
            sender=app.config['MAIL_USERNAME'],
            recipients=[emailToSend],
            body=message
        )
    except Exception:
        return str(Exception)
    return "success"


def sendForgotEmail(link, zID, emailToSend):
    message = f"""\
Hi,{zID}\nYou have requested to reset your password.\nFollow this link to reset your password: {link}"""

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

'''
def main():

    for i in range(0, 200):
        receiverEmail = f"z5{i:06d}@unsw.edu.au"
        sendActivationEmail("Yo wassup", receiverEmail)

        print(f"{receiverEmail} sent")

if __name__ == "__main__":
    main()
'''