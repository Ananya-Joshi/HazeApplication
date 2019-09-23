import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 10
db = SQLAlchemy(app)


def haze_alert():
	print('scheduler')
	global old_state
	now = datetime.datetime.now()
	val_25, val_day = haze_detect()
	print(val_25, val_day)
	alert = 0
	if ((val_25 > 56) or (val_day > 101)):
		if old_state is 0:
			alert = 1
			old_state = 1
	else:
		if old_state == 1:
			old_state = 0
	email_string = "Be advised that there is now (" + str(f'{now.hour:02}')  + ":" + str(f'{now.minute:02}')+ " ) a haze alert. Conditions are PSI25 - " + str(val_25) + " Daily - " + str(val_day)
	if alert:
		emails_try = list(Result.query.distinct())
		all_emails = []
		for email_each in emails_try:
			all_emails = all_emails + [email_each]
		print(all_emails)
		# for email_each in all_emails:
		# 	with app.app_context():
		# 	    msg = Message(subject="Haze Alert",
		# 	                  sender=app.config.get("MAIL_USERNAME"),
		# 	                  recipients=[email_each], # replace with your email for testing
		# 	                  body=email_string)
		# 	    mail.send(msg)
	alert = 0



if __name__ == "__main__":
	scheduler = BackgroundScheduler()
	job = scheduler.add_job(haze_alert, 'interval', seconds=5)
	scheduler.start()
	app.run(debug=True)



if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)