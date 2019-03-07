from main import db, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    avatar = db.Column(db.String(20), nullable = False, default = 'default.jpg')
    password = db.Column(db.String(60), nullable = False)
    is_owner = db.Column(db.Boolean, default = False)
    reservations = db.relationship('Reservation', backref="author", lazy=True)
    hotels = db.relationship('Hotel', backref='owner', lazy=True)


    #How object is printed
    def __repr__(self):
        return f"User('{self.username}, {self.email}, {self.avatar}')"


class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    check_in = db.Column(db.DateTime, nullable = False)
    check_out = db.Column(db.DateTime, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    hotel_info = db.Column(db.Integer, db.ForeignKey('hotel.id'), nullable=False)

    #How object is printed
    def __repr__(self):
        return f"Reservation('{self.check_in}, {self.check_out}, {self.user_id}, {self.id}, {self.hotel_info})"


class Hotel(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120), nullable = False)
    city = db.Column(db.String(120), nullable = False)
    state = db.Column(db.String(120), nullable = False)
    country = db.Column(db.String(120), nullable = False)
    rating = db.Column(db.Integer, nullable = False)
    price_cat = db.Column(db.String(5), nullable = False)
    price_night = db.Column(db.Integer, nullable = False)
    content = db.Column(db.Text, nullable=False)
    pic_1 = db.Column(db.String(20), nullable = False, default = 'hotel_default.jpg')
    #pic_2 = db.Column(db.String(20), nullable = True, default = 'default.jpg')
    #pic_3 = db.Column(db.String(20), nullable = True, default = 'default.jpg')
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reserved = db.relationship('Reservation', backref='reservation_made', lazy=True)

    #How object is printed
    def __repr__(self):
        return f"Hotel('{self.name}, {self.city}, {self.state}, {self.country}, {self.rating}, {self.price_cat}, {self.price_night}, {self.content}, {self.pic_1}, {self.reserved}')"
