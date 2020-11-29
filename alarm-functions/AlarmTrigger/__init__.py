import logging
import os
import azure.functions as func
import smtplib, ssl
from twilio.rest import Client

temperature_threshold = os.environ.get('TEMPERATURE_THRESHOLD', 30)

# Email configs
port = 587
smtp_server = "smtp.gmail.com"
sender_email = os.environ.get('EMAIL_FROM')
receiver_email = os.environ.get('EMAIL_TO')
password = os.environ.get('EMAIL_APP_PASSWORD')
context = ssl.create_default_context()


def main(documents: func.DocumentList) -> str:
    if not documents:
        return ''

    item = documents[0]
    if item.get('type', None) == 'temperature':
        temp = item.get('value', None)
        if temp <= 30:
            return ''

        send_email(temp)
        send_sms(temp)

    logging.info('Document id: %s', documents[0])


def send_email(temp):
    message = f"""\
    Subject: High Temperature Alarm: {temp}   

    Sensor has detected that temperature is as high as: {temp}."""

    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)


def send_sms(temp):
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
        body=f"Sensor has detected that temperature is as high as: {temp}",
        from_=os.environ['TWILIO_FROM'],
        to=os.environ['TWILIO_TO']
    )

    print(f'Twilio message sent with id {message.sid}')
