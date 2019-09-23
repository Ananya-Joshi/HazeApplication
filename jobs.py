from apscheduler.schedulers.background import BackgroundScheduler
from app import db, haze_detect, app
from models import *
from flask_mail import Mail, Message
import logging
import datetime
import os

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": os.environ['EMAIL_USER'],
    "MAIL_PASSWORD": os.environ['EMAIL_PASSWORD']
}


app.config.update(mail_settings)
mail = Mail(app)

# sched = BlockingScheduler()

# @sched.scheduled_job('interval', seconds=1)
# def haze_alert():
#   print('scheduler')
#   sys.stdout.flush()
#   old_state_a = Variable.query.filter_by(name = 'old_state').first()
#   old_state = old_state_a.value
#   #print("current state is", old_state)
#   now = datetime.datetime.now()
#   val_25, val_day = haze_detect()
#   #print(val_25, val_day)
#   alert = 0
#   if ((val_25 > 56) or (val_day > 101)):
#       if old_state is 0:
#           alert = 1
#           old_state = 1
#   else:
#       if old_state == 1:
#           old_state = 0
#   print('email alert', alert)
#   print('old_state NEW', old_state)
#   db.session.delete(old_state_a)
#   db.session.add(Variable("old_state", old_state))
#   db.session.commit()
#   email_string = "Be advised that there is now (" + str(f'{now.hour:02}')  + ":" + str(f'{now.minute:02}')+ " ) a haze alert. Conditions are PSI25 - " + str(val_25) + " Daily - " + str(val_day)
#   if alert:
#       emails_try = list(Result.query.distinct())
#       all_emails = []
#       for email_each in emails_try:
#           all_emails = all_emails + [email_each.email]
#       #print(all_emails)
#       for email_each in all_emails:
#           with app.app_context():
#               msg = Message(subject="Haze Alert",
#                             sender=app.config.get("MAIL_USERNAME"),
#                             recipients=[email_each], # replace with your email for testing
#                             body=email_string)
#               mail.send(msg)
#   alert = 0
    
# sched.start()


# sched = BackgroundScheduler(daemon=True)
# @sched.scheduled_job('interval',seconds=10)
# def haze_alert():
    
    # sys.stdout.flush()
    
    



# sched.start()


from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=1)
def timed_job():
    print('scheduler')
    if Variable.query.filter_by(name = 'old_state').first() is None:
        var = Variable(name = "old_state", value = 0)
        db.session.add(var)
        db.session.commit()
    old_state_a = Variable.query.filter_by(name = 'old_state').first()
    old_state = old_state_a.value
    print("current state is", old_state)
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
    print('email alert', alert)
    print('old_state NEW', old_state)
    db.session.delete(old_state_a) 
    db.session.add(Variable("old_state", old_state))
    db.session.commit()
    email_string = "Be advised that there is now (" + str(f'{now.hour:02}')  + ":" + str(f'{now.minute:02}')+ ") a haze alert. Conditions are PSI25 - " + str(val_25) + " Daily - " + str(val_day)
    email_string = email_string.encode('utf-8')
    if alert:
        emails_try = list(Result.query.distinct())
        all_emails = []
        for email_each in emails_try:
            all_emails = all_emails + [email_each.email]
        #print(all_emails)
        for email_each in all_emails:
            with app.app_context():
                msg = Message(subject="Haze Alert",
                              sender=app.config.get("MAIL_USERNAME"),
                              recipients=[email_each], # replace with your email for testing
                              body=email_string)
                print(msg.sender)
                mail.send(msg)
    alert = 0 

# @sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
# def scheduled_job():
#     print('This job is run every weekday at 5pm.')

sched.start()
# for i in range(10):
#     timed_job()

