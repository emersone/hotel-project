import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from main import app, db, bcrypt
from main.forms import RegisterForm, LoginForm, UpdateAccountForm, PostForm
from main.models import User, Hotel, Reservation
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/hotels')
@login_required
def hotels():
    posts = Hotel.query.all()
    return render_template('hotels.html', posts=posts)


#New user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title="Register", form=form)


#User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


#User logout
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


#User profile picture
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    #Resize image size
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path)

    return picture_fn

#User account information
@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.avatar = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated.', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    avatar = url_for('static', filename='profile_pics/' + current_user.avatar)
    return render_template('account.html', title='Account', avatar=avatar, form=form)


#User hotel reservations
@app.route('/reservations')
@login_required
def reservations():
    return render_template('reservations.html')


#Add a new hotel
#@app.route('/post/hotel', methods=['GET', 'POST'])
#@login_required
#def new_hotel():
#    form = PostForm()
#    if form.validate_on_submit():
#        post = PostForm(name=form.name.data, city=form.city.data, state=form.state.data, country=form.country.data, rating=form.rating.data, price_cat=form.price_cat.data, owner=current_user)
#        db.session.add(post)
#        db.session.commit()
#        flash('Your hotel has been added.', 'success')
#        return redirect(url_for('home'))
#    return render_template('create_hotel.html', title='New Hotel', form=form)



@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_hotel():
    form = PostForm()
    if form.validate_on_submit():
        post = Hotel(name=form.name.data, city=form.city.data, state=form.state.data, country=form.country.data, rating=form.rating.data, price_cat=form.price_cat.data)
        db.session.add(post)
        db.session.commit()
        flash('Your hotel has been added.', 'success')
        return redirect(url_for('hotels'))
    return render_template('create_hotel.html', title='Add Hotel',
                           form=form, legend='Add Hotel')
