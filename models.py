from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, current_user, UserMixin, login_required

db = SQLAlchemy()


class Admin(db.Model, UserMixin):
    a_id = db.Column(db.Integer(), primary_key=True)
    a_name = db.Column(db.String(50), nullable=False, unique=False)
    a_email = db.Column(db.String(100), nullable=False, unique=True)
    a_password = db.Column(db.String(50), nullable=False, unique=False)

    def get_id(self):
        return (self.a_id)


class User(db.Model, UserMixin):
    u_id = db.Column(db.Integer(), primary_key=True)
    u_name = db.Column(db.String(50), nullable=False, unique=False)
    u_email = db.Column(db.String(100), nullable=False, unique=True)
    u_password = db.Column(db.String(50), nullable=False, unique=False)
    b_book = db.relationship('Booking', backref='user')

    def get_id(self):
        return (self.u_id)


class Venue(db.Model):
    v_id = db.Column(db.Integer(), primary_key=True)
    v_name = db.Column(db.String(100), nullable=False)
    v_place = db.Column(db.String(100), nullable=False)
    v_location = db.Column(db.String(100), nullable=False)
    v_capacity = db.Column(db.Integer(), nullable=False)
    shows = db.relationship("Show", backref="s_venue")
    booking = db.relationship("Booking", backref="b_venue")


class Show(db.Model):
    s_id = db.Column(db.Integer(), primary_key=True)
    s_name = db.Column(db.String(100), nullable=False)
    s_starttime = db.Column(db.String(50), nullable=False)
    s_endtime = db.Column(db.String(50), nullable=False)
    s_ratings = db.Column(db.String(50), nullable=False)
    s_tags = db.Column(db.String(100), nullable=False)
    s_price = db.Column(db.Integer(), nullable=False)
    venue_id = db.Column(db.Integer(), db.ForeignKey('venue.v_id'))
    bookings = db.relationship("Booking", backref="show")


class Booking(db.Model):
    b_id = db.Column(db.Integer(), primary_key=True)
    b_seatsbooked = db.Column(db.Integer(), nullable=False)
    b_show = db.Column(db.Integer(), db.ForeignKey(
        'show.s_id'), nullable=False)
    vv_id = db.Column(db.Integer(), db.ForeignKey(
        'venue.v_id'), nullable=False)
    b_user = db.Column(db.Integer(), db.ForeignKey(
        'user.u_id'), nullable=False)
