# -*- coding: UTF-8 -*-
from flask import Flask, request, redirect, url_for,render_template, jsonify
from flask.ext.olinauth import OlinAuth, auth_required,current_user
import twilio.twiml
import os
from pymongo import MongoClient

import phonenumbers
import requests
import json

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import smtplib

import datetime
from pytz import timezone

app=Flask(__name__)

SECRET_KEY = "secret secret"

app.config.from_object(__name__)

if os.environ.get('MONGOLAB_URI',None):
	#we are in heroku, act accordingly
	app.config['mongodb_uri'] = os.environ['MONGOLAB_URI']
	print "the mongodb uri is %s" % app.config['mongodb_uri']
	client = MongoClient(app.config['mongodb_uri'])
	db = client['heroku_app15804168']
	oa = OlinAuth(app,'txt2helpme.herokuapp.com')
	oa.init_app(app,'txt2helpme.herokuapp.com')
else:
#we are local, debug mode.
	app.config['mongodb_uri'] = 'mongodb://localhost/txt2helpme' #set db uri
	client = MongoClient(app.config['mongodb_uri'])
	db = client['txt2helpme']
	oa = OlinAuth(app,'localhost:5000')
	oa.init_app(app,'localhost:5000')

try:
	db.authenticate("app","root")
except:
	db.logout()
	db.authenticate("app","root")

collection = db.txt2helpme


@app.route("/",methods=["GET"])
@auth_required
def home():
	olin_id = current_user["id"]
	print "I got the current user"
	try:
		user = collection.find_one({"olin_id" : olin_id})
	except:
		registered = False
		return render_template("index.html",registered=registered,register_success=False,register_fail=False,change_success=False,change_fail=False,id=olin_id)
	print "I can query!"
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

@app.route("/register",methods=["GET","POST"])
@auth_required
def register():
	olin_id = current_user["id"]
	if request.method == 'GET':
		try:
			user = collection.find_one({"olin_id" : olin_id})
		except:
			registered = False
			return render_template("index.html",registered=registered,register_success=False,register_fail=False,change_success=False,change_fail=False,id=olin_id)
		number = None
		name = None
		if user:
			registered = True
			number = user["number"]
			name = user["name"]
		else:
			registered = False
		return render_template("index.html",registered=registered,register_success=False,register_fail=False,change_success=False,change_fail=False,id=olin_id,number=number,name=name)
	else:
		raw_number = request.values.get('number',None)
		display_name = request.values.get('name',None)
		validated_number = validate_number(raw_number)
		print ">>>> the validated number is %s" % validated_number
		print ">>>> does the number exist? %s" % number_exists(validated_number)
		print ">>>> does the user exist? %s" % user_exists(olin_id)
		if validated_number and not number_exists(validated_number) and not user_exists(olin_id):
			new_user = {}
			new_user["number"] = validated_number
			new_user["name"] = display_name
			new_user["olin_id"] = olin_id
			collection.insert(new_user)
			return render_template("index.html",registered=True,register_success=True,register_fail=False,change_success=False,change_fail=False,id=olin_id,number=validated_number,name=display_name)
		else:
			return render_template("index.html",registered=False,register_success=False,register_fail=True,change_success=False,change_fail=False,id=olin_id)

# @app.route("/dining",methods=["GET"])
# def dining():
# 	d = get_meals()
# 	return str(d)

@app.route("/apply",methods=["GET","POST"])
@auth_required
def apply_changes():
	olin_id = current_user["id"]
	if request.method == 'GET':
		try:
			user = collection.find_one({"olin_id" : olin_id})
		except:
			registered = False
			return render_template("index.html",registered=registered,register_success=False,register_fail=False,change_success=False,change_fail=False,id=olin_id)
		number = None
		name = None
		if user:
			registered = True
			number = user["number"]
			name = user["name"]
		else:
			registered = False
		return render_template("index.html",registered=registered,register_success=False,register_fail=False,change_success=False,change_fail=False,id=olin_id,number=number,name=name)
	else:
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

@app.route("/text",methods=["GET","POST"])
def text():
	sender_number = request.values.get('From',None)
	sent_message = request.values.get('Body',None)
	print "message received from %s" % sender_number
	try:
		sender = collection.find_one({"number":sender_number})
		sender_name = sender["name"]
		send_email(sender_name, sender_number,sent_message)
		message = "Alright %s, your message has been sent. Your phone number, %s, was included in the email. Help is on the way!" % (sender_name,sender_number)
	except:
		message = "I'm sorry, I don't know who you are. Please register at txt2helpme.herokuapp.com"
	resp = twilio.twiml.Response()
	resp.sms(message)
	return str(resp)

@app.route("/meals",methods = ["POST"])
def meals():
	sender_number = request.values.get('From',None)
	sent_message = request.values.get('Body',None)
	print "message received from %s" % sender_number
	try:
		message = get_human_food(sent_message)
	except Exception as e:
		message = "I'm sorry, I don't know who you are. Please register at txt2helpme.herokuapp.com"
		raise e
	resp = twilio.twiml.Response()
	resp.sms(message)
	return str(resp)

def user_exists(olin_id):
	try:
		user = collection.find_one({"olin_id" : olin_id})
		if user:
			return True
		return False
	except:
		return False

def number_exists(number):
	try:
		user = collection.find_one({"number" : number})
		if user:
			return True
		return False
	except:
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

def send_email(name,number,message_text):

	# from email.mime.text import MIMEtext

	server = "smtp.gmail.com:587"
	sender = "txt2helpme@gmail.com"
	password = "olinhasnotrees"
	receiver = "helpme@lists.olin.edu"

	subject = "%s Needs Help!" % name

	message = MIMEMultipart('alternative')
	message['Subject'] = subject
	message['From'] = sender
	message['To'] = receiver

	formatted_number = phonenumbers.format_number(phonenumbers.parse(number,"US"),phonenumbers.PhoneNumberFormat.NATIONAL)

	plain_text_message = """ %s needs help and has sent the following message: \r\n

	%s\r\n\r\n

	You can reach %s by calling or texting %s.

	This message was generated by txt2helpme. 
	""" % (name,message_text, name, formatted_number)

	html_message = """<html>
	<head></head>
	<body> 
	<p> %s needs help and has sent the following message:</p>
	<p> %s </p>
	<p> You can reach %s by calling or texting %s.</p>
	<span>Brought to you by <a href="txt2helpme.herokuapp.com">Txt2HelpMe</a> </span>
	</body>
	</html>
	""" % (name,message_text,name,formatted_number)

	plain_text_part = MIMEText(plain_text_message,'plain')
	html_part = MIMEText(html_message,'html')

	message.attach(plain_text_part)
	message.attach(html_part)

	server = smtplib.SMTP(server)
	server.starttls()
	server.login("txt2helpme",password)
	server.sendmail(sender,receiver,message.as_string())
	server.sendmail(sender,sender,message.as_string())
	server.quit()

def get_meals():
	r = requests.get("http://olinapps-dining.herokuapp.com/api")	
	data = json.loads(r.text)
	return data


def to_food_list(food):
  items = []
  for meal_type_list in food.values():
    for meal_dict in meal_type_list:
      items.append(meal_dict["name"])
  return items

def today_is():
  days = {0:"monday",1:"tuesday",2:"wednesday",3:"thursday", 4:"friday", 5:"saturday", 6:"sunday"}
  eastern = timezone("US/Eastern")
  now = datetime.datetime.today().replace(tzinfo=eastern).weekday()
  return days[now]

def tomorrow_is():
  days = {0:"monday",1:"tuesday",2:"wednesday",3:"thursday", 4:"friday", 5:"saturday", 6:"sunday"}
  eastern = timezone("US/Eastern")
  now = (datetime.datetime.today().replace(tzinfo=eastern).weekday() + 1) % 7
  return days[now]

def parse_meal_request(text):
  day_requested = "monday"
  meal_requested = "lunch"
  weekdays = ["monday", "tuesday" , "wednesday" , "thursday", "friday"]
  meals = ["breakfast","lunch","dinner","brunch"]
  indices = { "monday" : 0, "tuesday" : 1, "wednesday" : 2, "thursday" : 3, "friday" : 4, "saturday": 5, "sunday" : 6 }
  weekday = False
  lower_text = text.lower()
  text = lower_text
  r = requests.get("http://olinapps-dining.herokuapp.com/api")  
  raw_text = r.text
  # raw_text.replace(u"Entrée",u"Entree")
  raw_text.replace(u"Entr\xe9e",u"Entree")
  meal_data = json.loads(raw_text)

  #is it a weekday? -> what day -> what meal?
  #is it the weekend? -> which day? -> brunch or dinner?
  if "today" in text or "tonight" in text: 
  	day_requested = today_is()
  elif "tomorrow" in text:
  	day_requested = tomorrow_is()
  else:
	  for day in weekdays:
	    if day in text:
	      weekday = True
	      day_requested = day
	  if not weekday:
	    if "saturday" in text:
	      day_requested = "saturday"
	    else:
	      day_requested = "sunday"
  if day_requested is None: # in case they didn't include a day, assume it's today
  	day_requested = today_is()
  if day_requested == "saturday" or day_requested == "sunday":
  	weekday = False
  else:
  	weekday = True
  if not weekday:
	if "dinner" in text:
	  meal_requested = "dinner"
	else:
	  meal_requested = "brunch"
  else:
    for meal in meals:
      if meal in text:
        meal_requested = meal
  food = meal_data[indices[day_requested]]
  if meal_requested == "brunch":
    if weekday:
      return "there is no brunch on weekdays!"
    brunch = to_food_list(food["breakfast"])
    brunch.extend(to_food_list(food["lunch"]))
    return brunch
  else:
    return to_food_list(food[meal_requested])

def humanize_food_list(food_list):
  food_list = map(lambda x: str(x),food_list)
  food_list.sort()
  humanized = ", ".join(food_list)
  return humanized

def get_human_food(text):
	return humanize_food_list(parse_meal_request(text))

if __name__ == '__main__':
    try:
        port = int(os.environ.get('PORT', 5000))
        app.run(host='0.0.0.0', port=port, debug=True)
    except Exception as e:
        app.logger.debug("%s"%e)