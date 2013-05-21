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
def hello_monkey():
	from_number = request.values.get('From',None)
	print request.values.get('Body','ooh fuck')
	if from_number in callers:
		message = "hello %s" % callers[from_number]
	else:
		message = "I don't know who you are"

	resp = twilio.twiml.Response()
	resp.sms(message)
	return str(resp)

if __name__ == '__main__':
    try:
        port = int(os.environ.get('PORT', 5000))
        app.run(host='0.0.0.0', port=port, debug=True)
    except Exception as e:
        app.logger.debug("%s"%e)