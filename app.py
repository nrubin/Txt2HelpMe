#the actual app

from flask import Flask, request, redirect
import twilio.twiml
import os

app=Flask(__name__)

@app.route("/",methods=["GET","POST"])
def hello_monkey():
	resp = twilio.twiml.Response()
	resp.sms("Hello, Mobile Monkey")
	return str(resp)

if __name__ == '__main__':
    try:
        port = int(os.environ.get('PORT', 5000))
        app.run(host='0.0.0.0', port=port, debug=True)
    except Exception as e:
        app.logger.debug("%s"%e)