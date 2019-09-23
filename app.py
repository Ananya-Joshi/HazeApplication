from flask import Flask, render_template, request, url_for, redirect
from urllib.request import urlopen
import json 
import datetime
from flask_mail import Mail, Message
import os
from flask_sqlalchemy import SQLAlchemy
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
import random
import sys
import logging
import atexit



app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 10
db = SQLAlchemy(app)
if 'DYNO' in os.environ:
    app.logger.addHandler(logging.StreamHandler(sys.stdout))
    app.logger.setLevel(logging.ERROR)




def haze_detect():
	print("date update")
	now = datetime.datetime.now()
	string_In = str(now.year) + "-" + str(f'{now.month:02}') + "-" + str(f'{now.day:02}')  + "T" + str(f'{now.hour:02}')  + "%3A" + str(f'{now.minute:02}')  + "%3A" + str(f'{now.second:02}') 
	#print(string_In)
	url = "https://api.data.gov.sg/v1/environment/pm25?date_time=" + string_In
	url2 = "https://api.data.gov.sg/v1/environment/psi?date_time=" + string_In
	#local haze
	geo_xml = urlopen(url)
	datastore = json.load(geo_xml)
	#print(datastore)
	# print(json.dumps(datastore, indent=4, sort_keys=True))
	tmpDict = datastore["items"][0]
	val_25 = tmpDict['readings']['pm25_one_hourly']['west']
	#24 hour PSI
	geo_xml2 = urlopen(url2)
	datastore2 = json.load(geo_xml2)
	tmpDict = datastore2["items"][0]
	val_day = tmpDict['readings']["psi_twenty_four_hourly"]['west']
	return (val_25, val_day)
	# return(random.randrange(0,100),random.randrange(80,120))

@app.route("/")
def haze():
	val_25, val_day = haze_detect()
	if ((val_25 > 56) or (val_day > 101)):
		haze = "linear-gradient(to top left, red, white)"
	else:
		haze = "linear-gradient(to top left, lightgreen, white)"
	data = [haze, val_25, val_day]
	return render_template("bgIm.html" , haze=data)


# @app.route("/_haze_alert" , methods = ['GET', 'POST'])
# def haze_alert():
# 	now = datetime.datetime.now()
# 	string_In = str(now.year) + "-" + str(f'{now.month:02}') + "-" + str(f'{now.day:02}')  + "T" + str(f'{now.hour:02}')  + "%3A" + str(f'{now.minute:02}')  + "%3A" + str(f'{now.second:02}') 
# 	print(string_In)
# 	url = "https://api.data.gov.sg/v1/environment/pm25?date_time=" + string_In
# 	url2 = "https://api.data.gov.sg/v1/environment/psi?date_time=" + string_In
# 	#local haze
# 	geo_xml = urlopen(url)
# 	datastore = json.load(geo_xml)
# 	print(datastore)
# 	# print(json.dumps(datastore, indent=4, sort_keys=True))
# 	tmpDict = datastore["items"][0]
# 	val_25 = tmpDict['readings']['pm25_one_hourly']['west']
# 	#24 hour PSI
# 	geo_xml2 = urlopen(url2)
# 	datastore2 = json.load(geo_xml2)
# 	tmpDict = datastore2["items"][0]
# 	val_day = tmpDict['readings']["psi_twenty_four_hourly"]['west']
# 	if ((val_25 > 56) or (val_day > 101)):
# 		haze = 1
# 	else:
# 		haze = 0
# 	return render_template("bgIm.html" , haze=haze)


from models import *


@app.route('/addEmail', methods=['POST', 'GET'])
def addEmail():
	if request.method == 'POST':
	    old_email = request.form.get('email')
	    entry = Result(
	        email=old_email
	    )
	    if not (bool(Result.query.filter_by(email=old_email).first())):
		    db.session.add(entry)
		    db.session.commit()
	return redirect(url_for('haze'))


# sched = BackgroundScheduler(daemon=True)
# @sched.scheduled_job('interval',seconds=1)
# def haze_alert():
# 	print('scheduler')
# 	sys.stdout.flush()
# 	old_state_a = Variable.query.filter_by(name = 'old_state').first()
# 	old_state = old_state_a.value
# 	print("current state is", old_state)
# 	now = datetime.datetime.now()
# 	val_25, val_day = haze_detect()
# 	print(val_25, val_day)
# 	alert = 0
# 	if ((val_25 > 56) or (val_day > 101)):
# 		if old_state is 0:
# 			alert = 1
# 			old_state = 1
# 	else:
# 		if old_state == 1:
# 			old_state = 0
# 	print('email alert', alert)
# 	print('old_state NEW', old_state)
# 	db.session.delete(old_state_a)
# 	db.session.add(Variable("old_state", old_state))
# 	db.session.commit()
# 	email_string = "Be advised that there is now (" + str(f'{now.hour:02}')  + ":" + str(f'{now.minute:02}')+ " ) a haze alert. Conditions are PSI25 - " + str(val_25) + " Daily - " + str(val_day)
# 	email_string = email_string.encode('utf-8')
# 	if alert:
# 		emails_try = list(Result.query.distinct())
# 		all_emails = []
# 		for email_each in emails_try:
# 			all_emails = all_emails + [email_each.email]
# 		#print(all_emails)
# 		for email_each in all_emails:
# 			with app.app_context():
# 			    msg = Message(subject="Haze Alert",
# 			                  sender=app.config.get("MAIL_USERNAME"),
# 			                  recipients=[email_each], # replace with your email for testing
# 			                  body="email_string")
# 			    print(msg.sender)
# 			    mail.send(msg)
# 	alert = 0






if __name__ == "__main__":
	if not bool(Variable.query.filter_by(name = 'old_state').first()):
		var = Variable(name = "old_state", value = 0)
		db.session.add(var)
		db.session.commit()
	# sched.start()
	app.run(debug=True)





