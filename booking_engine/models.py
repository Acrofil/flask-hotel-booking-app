from booking_engine import db
from datetime import datetime

# Admin model
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    admin = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)

    def __repr__(self):
        return '<Admin %r>' % self.admin

# Room model with relationships for listed_room and reservation
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
    # Create relationship - on to many with Reservation
    reservation = db.relationship("Reservation", backref='room')

# RateType model with relationships between rate_plan and listed_room
class RateType(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    rate_name = db.Column(db.String(50), nullable=False)
    # Create relationship with rate_plan table
    rate_plan_type = db.relationship('RatePlan', backref='rate_type')
    # Relationship with ListedRoom
    listed_room = db.relationship("ListedRoom", backref='rate_type')

# RatePlan model with set foreign key to rate_type
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

# ListedRoom model with relationship for room_availability and foreign keys for rate_type and room
class ListedRoom(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    listed_date = db.Column(db.DateTime, nullable=False)
    quantity_per_date = db.Column(db.Integer, nullable=False)
    # Foreign keys for rate_type and room
    rate_type_id = db.Column(db.Integer, db.ForeignKey('rate_type.id'))
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    # Relationship between room_availability and listed_room
    room_availability = db.relationship('RoomAvailability', backref='listed_room')

# RoomAvailability model with foreign key for listed_room
class RoomAvailability(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    left_to_sell = db.Column(db.Integer, nullable=False)
    booked_quantity = db.Column(db.Integer, nullable=True)
    is_it_available = db.Column(db.Boolean, nullable=False, default=True)
    listed_room_id = db.Column(db.Integer, db.ForeignKey('listed_room.id'), nullable=False)


# Creating table bookings and many to many relationship between them
bookings = db.Table('bookings',
        db.Column('client_id', db.Integer, db.ForeignKey('client.id')),
        db.Column('reservation_id', db.Integer, db.ForeignKey('reservation.id'))
)


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    # Create relationship between Client, Bookings and Reservation
    # backref will create refference in Reservations named reservations
    reservation = db.relationship("Reservation", secondary=bookings, backref='reservations')


class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    reservation_number = db.Column(db.Integer, nullable=False, unique=True)
    check_in = db.Column(db.DateTime, nullable=False)
    check_in_time = db.Column(db.DateTime, nullable=True)
    check_out = db.Column(db.DateTime, nullable=False)
    total_days = db.Column(db.Integer, nullable=False)
    total_rooms_reserved = db.Column(db.Integer, nullable=False)
    total_guests = db.Column(db.Integer, nullable=False)
    total_adults = db.Column(db.Integer, nullable=False)
    total_children = db.Column(db.Integer, nullable=True)
    children_age = db.Column(db.String(100), nullable=True)
    note = db.Column(db.String(250), nullable=True)
    room_price_day = db.Column(db.Integer, nullable=False)
    all_rooms_price_day = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)
    # Foreign key to link reservation with room
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))

