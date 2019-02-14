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
    reservations = db.relationship('Reservation', backref = 'owner', lazy = True)

    #How object is printed
    def __repr__(self):
        return f"User('{self.username}, {self.email}, {self.avatar}')"

class Hotel(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120), nullable = False)
    city = db.Column(db.String(120), nullable = False)
    state = db.Column(db.String(120), nullable = False)
    country = db.Column(db.String(120), nullable = False)
    rating = db.Column(db.Integer, nullable = False)
    price_cat = db.Column(db.String(5), nullable = False)
    #content = db.Column(db.Text, nullable = False)

    #How object is printed
    def __repr__(self):
        return f"Hotel('{self.name}, {self.city}, {self.state}, {self.country}, {self.rating}, {self.price_cat}, {self.content}')"

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    date_made = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

    #How object is printed
    def __repr__(self):
        return f"Reservation('{self.date_made}', {self.user_id})"
