#let's first try usingt the Twilio API
# from twilio.rest import TwilioRestClient

# account = "ACd157e0b975d385b6a3c5e75d1dfe3ada"
# token = "321a73a952e221c475bea034f9328bf5"

# client = TwilioRestClient(account,token)

# recipient = "3104299195"
# sender = "13107766978"
# body = "This is a message from Noam"

# message = client.sms.messages.create(to=recipient,from_=sender,body=body)

import smtplib

# from email.mime.text import MIMEtext

server = "smtp.gmail.com:587"
sender = "rubin.m.noam@gmail.com"
password = "Gnb4jvyeamaq4"
receiver = ["noam@outlook.com"]

subject = "hello"
text = "world"

message = """From: %s\r\nTo: %s\r\nSubject: %s\r\n\

%s
""" % (sender, ", ".join(receiver), subject, text)

server = smtplib.SMTP(server)
server.starttls()
server.login("rubin.m.noam",password)
server.sendmail(sender,receiver,message)
server.quit()
# server.sendmail(sender,receiver,message)
# server.quit()

