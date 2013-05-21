#the actual app

from flask import Flask, request, redirect
import twilio.twiml
import os

app=Flask(__name__)

callers = {"+3104299195": "Noam"}

@app.route("/",methods=["GET"])
def home():
	return "hello, there is nothing here."

@app.route("/text",methods=["GET","POST"])
def text():
	sender_number = request.values.get('From',None)
	print "message received from %s" % sender_number
	sender_name = callers.get(sender_number,'anonymous')
	sent_message = request.values.get('Body',None)

	if sent_message:
		send_email(sender_name, sent_message)

	if sender_number in callers:
		message = "hello %s" % callers[sender_number]
	else:
		message = "I don't know who you are"

	resp = twilio.twiml.Response()
	resp.sms(message)
	return str(resp)

def send_email(name,message):
	import smtplib

	# from email.mime.text import MIMEtext

	server = "smtp.gmail.com:587"
	sender = "txt2helpme@gmail.com"
	password = "olinhasnotrees"
	receiver = ["noam@outlook.com"]

	subject = "%s Needs Help!" % name

	email = """From: %s\r\nTo: %s\r\nSubject: %s\r\n\

	%s
	""" % (sender, ", ".join(receiver), subject, message)

	server = smtplib.SMTP(server)
	server.starttls()
	server.login("txt2helpme",password)
	server.sendmail(sender,receiver,email)
	server.quit()
	# server.sendmail(sender,receiver,message)
	# server.quit()



if __name__ == '__main__':
    try:
        port = int(os.environ.get('PORT', 5000))
        app.run(host='0.0.0.0', port=port, debug=True)
    except Exception as e:
        app.logger.debug("%s"%e)