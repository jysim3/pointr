import os
from app import app
from threading import Thread
from email.mime.multipart  import MIMEMultipart
from email.mime.text  import MIMEText
import smtplib
from util.mail_template import get_login_mail_template

site = 'https://pointr.live'
server = smtplib.SMTP()
if app.config['ENV'] == 'production':
    server.connect('localhost')
    server.ehlo()
else:
    pass
server.set_debuglevel(3)
app.config.update(
    MAIL_USERNAME = "main@pointr.live"
)


def sendAsyncMail(app, msg, recipients):
    with app.app_context():
        try:
            from_email = app.config['MAIL_USERNAME']
            server.sendmail(from_email, recipients, msg.as_string())
        except smtplib.SMTPServerDisconnected as e:
            if app.config['ENV'] != 'development':
                raise e
            print('Sending email does not work in dev...')
        except smtplib.SMTPException as e:
            server.connect('localhost')
            server.ehlo()
            from_email = app.config['MAIL_USERNAME']
            server.sendmail(from_email, recipients, msg.as_string())
            print(e)
            return str(e)

def createEmailBody(subject="",sender=app.config['MAIL_USERNAME'], recipients=[], html='', plain=''):
    if subject == "" or recipients == [] or (html == "" and plain == ""):
        raise ValueError()
    message = MIMEMultipart('alternative')
    message['Subject'] = subject
    message['From'] = f"Pointr <{sender}>"
    message['To'] = ','.join(recipients)
    message.attach( MIMEText( html, 'html') ) # TODO: Add real html body: jysim3
    return message



def sendActivationEmail(stringToSend, emailToSend, firstname):
    body = f"""Hello {firstname},<br/><br/>It's good to have you with us. Thanks again for signing up with Pointr.<br/><br/>Activate your account now: """
    message = createEmailBody(
            subject   = 'Activate Your Pointr Account',
            recipients = [f"{emailToSend}@ad.unsw.edu.au"],
            html      = get_login_mail_template(body, f"{site}/activate/{stringToSend}", "Activate Account")
            )
    # Async version
    Thread(target=sendAsyncMail, args=(app, message, message['To'])).start()
    #mail.send(message)
    return "success"


def sendForgotEmail(link, zID):
    body = f"""\
Hi {zID},<br/>You have requested to reset your password.<br/>Follow this link to reset your password:"""
    message = createEmailBody(
            subject   = 'Reset Your Pointr Password',
            recipients = [f"{zID}@ad.unsw.edu.au"],
            html      = get_login_mail_template(body, f"{site}/reset/{link}", "Reset Password")
            )

    # Async version
    Thread(target=sendAsyncMail, args=(app, message, message['To'])).start()
    return "success"

def sendEnquiry(sender, content):
    recipients=["stevenshen1999@hotmail.com", "steynharrison1@gmail.com", "junyang.0607@gmail.com", "hello@ivanvelickovic.com"]
    body = f"""
        Hello there,
        {sender} has send an enquiry about pointr:

        {content}

        Regards
    """
    message = createEmailBody(
            subject   = 'Enquire Email For Pointr',
            recipients= recipients,
            html      = body,
            plain     = body
            )


    # Async version
    Thread(target=sendAsyncMail, args=(app, message, recipients)).start()
    return "success"

'''
def main():

    for i in range(0, 200):
        receiverEmail = f"z5{i:06d}@unsw.edu.au"
        sendActivationEmail("Yo wassup", receiverEmail)

        print(f"{receiverEmail} sent")

'''
def main():
    sendActivationEmail('z5161631', 'z5161631', 'hello')
if __name__ == "__main__":
    main()
