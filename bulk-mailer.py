#!/usr/bin/env python3
## Bulk emailer for EngineeringX course
## Originally from https://levelup.gitconnected.com/sending-bulk-emails-via-python-4592b7ee57a5
## For sending while not on the RU network, you will need to use the SSL/TLS capability.  DON'T SHARE YOUR PASSWORD!

## TODO:  move credentials to another file
## TODO:  command line options and interface for sending

# Import smtplib for our actual email sending function
import smtplib
 
# Helper email modules 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# sender email address
email_user = 'foley@ru.is'
 
# sender email passowrd for login purposes
email_password = 'SENDER_EMAIL_PASSWORD'

# list of users to whom email is to be sent
email_send = ['foley@ru.is']
subject = 'Test Subject'
msg = MIMEMultipart()
msg['From'] = email_user
# converting list of recipients into comma separated string
msg['To'] = ", ".join(email_send)
msg['Subject'] = subject
body = 'THIS IS A TEST'
msg.attach(MIMEText(body,'plain'))
text = msg.as_string()
#server = smtplib.SMTP('smtp.ru.is',587)
server = smtplib.SMTP('smtp.ru.is')

## TLS/SSL support (if needed)
#server.starttls()
#server.login(email_user,email_password)

server.sendmail(email_user,email_send,text)
server.quit()
