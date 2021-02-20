from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

"""
Note class (entity) used to store notes that a user inputs once they log in to the website. 
Each note has: 

id: primary key
data: input from user
date: timestamp from moment user enters Note on website
user_id: associated w/ the user who is logged in that adds a note.  
"""


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


"""
User class (entity) used to store information about our users that register via the website. 
Each note has: 

id: primary key
email: input from user
password: user's password
first_name: user's first name
notes: relationship set that is able to join Note relation with User relation ON Note.user_id = User.id  
"""


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
