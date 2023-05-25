import os
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'CS50X-HOTEL-BOOKING-ENGINE-SECRET-PASSWORD!@##$#%$#434343-43-443434-...//'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///" +os.path.join(basedir, "hotel.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.debug = True
app.app_context().push()

from booking_engine import routes
