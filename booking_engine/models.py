from booking_engine import db
from datetime import datetime


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    admin = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)

    def __repr__(self):
        return '<Admin %r>' % self.admin

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(100), unique=True, nullable=False)
    max_guests = db.Column(db.Integer, nullable=False)
    max_adults = db.Column(db.Integer, nullable=False)
    max_children = db.Column(db.Integer, nullable=False)
    total_of_this_type = db.Column(db.Integer, nullable=False)
    room_image = db.Column(db.String(250), nullable=True)
    