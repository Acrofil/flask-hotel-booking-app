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
    min_guests = db.Column(db.Integer,)
    max_adults = db.Column(db.Integer, nullable=False)
    max_children = db.Column(db.Integer, nullable=False)
    total_of_this_type = db.Column(db.Integer, nullable=False)
    room_image = db.Column(db.String(), nullable=True)
    room_description = db.Column(db.String(), nullable=True)
    # Create relationship - One to many with RatePlan and refer to room table
    listed_room = db.relationship("ListedRoom", backref='room')


class RateType(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    rate_name = db.Column(db.String(50), nullable=False)
    # Create relationship with rate_plan table
    rate_plan_type = db.relationship('RatePlan', backref='rate_type')
    # Relationship with ListedRoom
    listed_room = db.relationship("ListedRoom", backref='rate_type')

# exb - extra bed, rb - regular bed
class RatePlan(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    adult = db.Column(db.Integer, nullable=False)
    single_adult = db.Column(db.Integer, nullable=False)
    child_under_12_rb = db.Column(db.Integer, nullable=False)
    child_under_18_exb = db.Column(db.Integer, nullable=True)
    child_under_12_exb = db.Column(db.Integer, nullable=True)
    child_under_7_exb = db.Column(db.Integer, nullable=True)
    child_under_2_exb = db.Column(db.Integer, nullable=True)
    from_date = db.Column(db.DateTime, nullable=False)
    to_date = db.Column(db.DateTime, nullable=False)
    # Foreign key to link rate_plan with rate_type by id
    rate_type_id = db.Column(db.Integer, db.ForeignKey('rate_type.id'))


class ListedRoom(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    listed_date = db.Column(db.DateTime, nullable=False)
    quantity_per_date = db.Column(db.Integer, nullable=False)
    # Foreign keys for rate_type and room
    rate_type_id = db.Column(db.Integer, db.ForeignKey('rate_type.id'))
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    # Relationship between room_availability and listed_room
    room_availability = db.relationship('RoomAvailability', backref='listed_room')


class RoomAvailability(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    left_to_sell = db.Column(db.Integer, nullable=False)
    booked_quantity = db.Column(db.Integer, nullable=False)
    is_it_available = db.Column(db.Boolean, nullable=False, default=False)
    listed_room_id = db.Column(db.Integer, db.ForeignKey('listed_room.id'), nullable=False)


