import os
from flask import Flask, request
from celery import Celery
import smtplib
from datetime import datetime
import logging

app = Flask(__name__)

# Configure Celery
app.config['CELERY_BROKER_URL'] = 'pyamqp://guest@localhost//'
app.config['CELERY_RESULT_BACKEND'] = 'rpc://'
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# Configure logging
log_file = os.path.join(os.path.expanduser('~'), 'messaging_system.log')
logging.basicConfig(filename=log_file, level=logging.INFO)

@celery.task
def send_email(recipient):
    # Implement the email sending logic here
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "techlab.activate@gmail.com"
    sender_password = "@HNG112024!"

    message = f"""\
    Subject: Test Email

    This is a test email to {recipient}."""

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient, message)

@app.route('/')
def index():
    sendmail = request.args.get('sendmail')
    talktome = request.args.get('talktome')

    if sendmail:
        send_email.apply_async(args=[sendmail])
        return f"Email queued to be sent to {sendmail}"
    
    if talktome:
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        logging.info(f"Current time logged: {current_time}")
        return f"Logged current time: {current_time}"

    return "Hello, World!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
