# HazeApplication

A simple Flask application with a database and clock that alerts users when there is a new haze advisory from the NEA near NUS. Available at https://haze-nus.herokuapp.com. 

# To Use

There are 4 environment variables you must set yourself: 
 1. export APP_SETTINGS="config.DevelopmentConfig"
 2. export DATABASE_URL="YOURDATABASE"
 3. export EMAIL_USER=YOUR_EMAIL
 4. export EMAIL_PASSWORD=YOUR_PASSWORD


# Resources Used:
https://www.haze.gov.sg/
https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xxi-user-notifications
https://realpython.com/flask-by-example-part-2-postgres-sqlalchemy-and-alembic/
https://www.twilio.com/blog/2018/03/send-email-programmatically-with-gmail-python-and-flask.html
https://devcenter.heroku.com/articles/clock-processes-python
