#the actual app

from flask import Flask, request, redirect, url_for,render_template
from flask.ext.olinauth import OlinAuth, auth_required,current_user
import twilio.twiml
import os
from pymongo import MongoClient

import phonenumbers


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import smtplib

app=Flask(__name__)

SECRET_KEY = "secret secret"

app.config.from_object(__name__)

try:
    app.config['mongodb_uri'] = os.environ['MONGOLAB_URI']
    client = MongoClient(app.config['mongodb_uri'],27318)
except Exception, e:
    app.config['mongodb_uri'] = 'mongodb://localhost/txt2helpme' #set db uri
    client = MongoClient(app.config['mongodb_uri'],27017)


db = client['txt2helpme']
collection = db.txt2helpme

if os.environ.get('PORT',None):
	oa = OlinAuth(app,'txt2helpme.herokuapp.com')
	oa.init_app(app,'txt2helpme.herokuapp.com')
else:
	oa = OlinAuth(app,'localhost:5000')
	oa.init_app(app,'localhost:5000')

callers = {"+13104299195": "Noam"}

@app.route("/",methods=["GET"])
@auth_required
def home():
	olin_id = current_user["id"]
	user = collection.find_one({"olin_id" : olin_id})
	print olin_id
	print user
	number = None
	name = None
	if user:
		registered = True
		number = user["number"]
		name = user["name"]
	else:
		registered = False
	return render_template("index.html",registered=registered,register_success=False,register_fail=False,change_success=False,change_fail=False,id=olin_id,number=number,name=name)

@app.route("/register",methods=["POST"])
@auth_required
def register():
	raw_number = request.values.get('number',None)
	display_name = request.values.get('name',None)
	validated_number = validate_number(raw_number)
	olin_id = current_user["id"]
	if validated_number and not number_exists(validated_number) and not user_exists(olin_id):
		new_user = {}
		new_user["number"] = validated_number
		new_user["name"] = display_name
		new_user["olin_id"] = olin_id
		collection.insert(new_user)
		return render_template("index.html",registered=True,register_success=True,register_fail=False,change_success=False,change_fail=False,id=olin_id,number=validated_number,name=display_name)
	else:
		return render_template("index.html",registered=False,register_success=False,register_fail=True,change_success=False,change_fail=False,id=olin_id)

@app.route("/apply",methods=["POST"])
@auth_required
def apply_changes():
	raw_number = request.values.get('number',None)
	display_name = request.values.get('name',None)
	validated_number = validate_number(raw_number)
	olin_id = current_user["id"]
	if validated_number:
		new_user = {}
		new_user["number"] = validated_number
		new_user["name"] = display_name
		new_user["olin_id"] = olin_id
		collection.update({"olin_id" : olin_id},new_user,upsert=True)
		print "the new user is %s" % (new_user)
		return render_template("index.html",registered=True,register_success=False,register_fail=False,change_success=True,change_fail=False,id=olin_id,number=validated_number,name=display_name)
	else:
		user = collection.find_one({"olin_id" : olin_id})
		number = user["number"]
		name = user["name"]
		return render_template("index.html",registered=True,register_success=False,register_fail=False,change_success=False,change_fail=True,id=olin_id,number=number,name=name)

def user_exists(olin_id):
	user = collection.find_one({"olin_id" : olin_id})
	if user:
		return True
	else:
		return False

def number_exists(number):
	user = collection.find_one({"number" : number})
	if user:
		return True
	else:
		return False

def validate_number(raw_number):
	"""
	tries to validate the incoming number. Returns the number formatted in a way Twilio likes if it works, or None if it doesn't.
	"""
	try:
		parsed_number = phonenumbers.parse(raw_number,"US")
		if phonenumbers.is_possible_number(parsed_number) and phonenumbers.is_valid_number(parsed_number):
			formatted_number = phonenumbers.format_number(parsed_number,phonenumbers.PhoneNumberFormat.E164)
			return formatted_number
		else:
			return None
	except:
		return None

# @app.route("/login",methods=["GET","POST"])
# @auth_required
# def login():
# 	olin_username = current_user["id"]
# 	user = collection.find_one({"olin_username":olin_username})
# 	if user:
# 		return "you have logged in"
# 	else:
# 		return redirect(url_for("register"))





@app.route("/text",methods=["GET","POST"])
def text():
	sender_number = request.values.get('From',None)
	print "message received from %s" % sender_number
	sender = collection.find_one({"number":sender_number})
	sender_name = sender["name"]
	sent_message = request.values.get('Body',None)

	if sent_message:
		send_email(sender_name, sent_message)

	if sender_number in callers:
		message = "Alright %s, your message has been sent. Help is on the way!" % sender_name
	else:
		message = "I'm sorry, I don't know who you are. Please register at txt2helpme.herokuapp.com"

	resp = twilio.twiml.Response()
	resp.sms(message)
	return str(resp)

def send_email(name,message_text):

	# from email.mime.text import MIMEtext

	server = "smtp.gmail.com:587"
	sender = "txt2helpme@gmail.com"
	password = "olinhasnotrees"
	receiver = "noam@outlook.com"

	subject = "%s Needs Help!" % name

	message = MIMEMultipart('alternative')
	message['Subject'] = subject
	message['From'] = sender
	message['To'] = receiver

	plain_text_message = """ %s needs help and has sent the following message: \r\n

	%s\r\n\r\n

	This message was generated by txt2helpme
	""" % (name,message_text)

	html_message = """<html>
	<head></head>
	<body> 
	<p> %s needs help and has sent the following message:</p>
	<p> %s </p>
	<span>Brought to you by <a href="txt2helpme.herokuapp.com">Txt2HelpMe</a> </span>
	</body>
	</html>
	""" % (name,message_text)

	plain_text_part = MIMEText(plain_text_message,'plain')
	html_part = MIMEText(html_message,'html')

	message.attach(plain_text_part)
	message.attach(html_part)

	server = smtplib.SMTP(server)
	server.starttls()
	server.login("txt2helpme",password)
	server.sendmail(sender,receiver,message.as_string())
	server.quit()
	# server.sendmail(sender,receiver,message)
	# server.quit()



if __name__ == '__main__':
    try:
        port = int(os.environ.get('PORT', 5000))
        app.run(host='0.0.0.0', port=port, debug=True)
    except Exception as e:
        app.logger.debug("%s"%e)