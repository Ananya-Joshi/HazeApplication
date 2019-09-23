from app import db
from sqlalchemy.dialects.postgresql import JSON

class Result(db.Model):
    __tablename__ = 'results'

    email = db.Column(db.String(), primary_key=True)
    


    def __init__(self, email):
        self.email = email


    def __repr__(self):
        return str(self.email)

class Variable(db.Model):
    __tablename__ ='variable'
    

    name = db.Column(db.String(), primary_key=True)
    value = db.Column(db.Integer())

    def __init__(self, name, value):
        self.name = name
        self.value = value


    def __repr__(self):
        return str(self.name)