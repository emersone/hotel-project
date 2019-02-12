from flask import Flask, render_template, current_app, request, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegisterForm, LoginForm
import logging
app = Flask(__name__)

app.config['SECRET_KEY'] = '89rAZOpeZSqGTsYal0z9'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

#Base code from: Youtuber Corey Schafer's Python Flask Tutorial series



#--------------------- Controller Functions ---------------------#
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/hotels')
def hotels():

    content = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam et pharetra velit, quis fermentum nisl. Donec quis est velit."

    hotels = [
        {
            'name': "Luxury Hotel",
            'city': "Beverly Hills",
            'state': "CA",
            'country': "USA",
            'content': content
        },
        {
            'name': "Tropical Paradise",
            'city': "Papeete",
            'state': "Bora Bora",
            'country': "French Polynesia",
            'content': content
        },
        {
            'name': "Winter Lodge",
            'city': "Whistler",
            'state': "BC",
            'country': "Canada",
            'content': content
        },
        {
            'name': "Modern Stay",
            'city': "New York City",
            'state': "NY",
            'country': "USA",
            'content': content
        }
    ]
    # entities, next_cursor = list_of_hotels()
    return render_template('hotels.html', hotels=hotels)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title="Register", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You are logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Username and/or password is incorrect.', 'danger')
    return render_template('login.html', title="Login", form=form)

@app.route('/reservations')
def reservations():
    return render_template('reservations.html')


if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)
