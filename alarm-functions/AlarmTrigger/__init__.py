import logging
import os
import azure.functions as func
import smtplib, ssl

port = 587
smtp_server = "smtp.gmail.com"
sender_email = os.environ.get('EMAIL_FROM')
receiver_email = os.environ.get('EMAIL_TO')
password = os.environ.get('EMAIL_APP_PASSWORD')
context = ssl.create_default_context()


def main(documents: func.DocumentList) -> str:
    if not documents:
        return ''

    twilio_account_sid = os.environ.get('TWILIO_ACCONT_SID')
    twilio_auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    email_password = os.environ.get('EMAIL_APP_PASSWORD')

    item = documents[0]
    if item.get('type', None) == 'temperature':
        temp = item.get('value', None)
        if temp <= 30:
            return ''

        send_email('Temperature is {}'.format(temp))

    logging.info('Document id: %s', documents[0])


def send_email(message):
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)