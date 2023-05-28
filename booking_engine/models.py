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
    room_image = db.Column(db.String(), nullable=True)
    room_description = db.Column(db.String(), nullable=True)
    # Create relationship - One to many with RatePlan and refer to room table
    #rate_plans = db.relationship('RatePlan', backref='room')


class RateType(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    rate_type = db.Column(db.String(), nullable=False)
    # Create relationship with rate_plan table
    rate_plan_type = db.relationship('RatePlan', backref='rate_type')


class RatePlan(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    rate_adult = db.Column(db.Integer, nullable=False)
    rate_child_under_12 = db.Column(db.Integer, nullable=False)
    rate_child_under_7 = db.Column(db.Integer, nullable=False)
    rate_child_under_2 = db.Column(db.Integer, nullable=False)
    from_date = db.Column(db.DateTime, nullable=False)
    to_date = db.Column(db.DateTime, nullable=False)
    # Foreign key to link rate_plan with rate_type by id
    rate_type_id = db.Column(db.Integer, db.ForeignKey('rate_type.id'))


"""
class RatePlanRange(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    rate_plan_ = db.Column(db.DateTime, nullable=False)
    rate_plan_end_date = db.Column(db.DateTime, nullable=False)
    # Foreign key to link RatePlan - refer to primary key
    rate_plan_id = db.Column(db.Integer, db.ForeignKey('rate_plan.id'))
    # Create relationship with RatePlanPrice
    rate_plan_price = db.relationship('RatePlanPrice', backref='rate_plan_range')


class RatePlanPrice(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    price_per_adult = db.Column(db.Integer, nullable=False)
    price_per_children_under_12 = db.Column(db.Integer, nullable=False)
    price_per_children_under_7 = db.Column(db.Integer, nullable=False)
    price_per_children_under_2 = db.Column(db.Integer, nullable=False)
    # Foreign key to link RatePlanRange - refer to primary key
    rate_plan_range_id = db.Column(db.Integer, db.ForeignKey('rate_plan_range.id'))


"""