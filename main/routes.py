import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from main import app, db, bcrypt
from main.forms import RegisterForm, LoginForm, UpdateAccountForm, PostForm, ReservationForm
from main.models import User, Hotel, Reservation
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/owner_home')
def owner_home():

    posts = db.session.query(Hotel).join(User, Hotel.owner_id==User.id)
    return render_template('owner_home.html', posts=posts)


@app.route('/hotels')
@login_required
def hotels():
    posts = Hotel.query.all()
    return render_template('hotels.html', posts=posts)


#New user and owner registration
@app.route('/register', methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterForm()

    if form.type.data == 'owner':
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data, email=form.email.data, password=hashed_password, is_owner=True)
            db.session.add(user)
            db.session.commit()
            flash('Your Hotel Owner account has been created.', 'success')
            return redirect(url_for('login'))
    else:
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data, email=form.email.data, password=hashed_password, is_owner=False)
            db.session.add(user)
            db.session.commit()
            flash('Your User account has been created.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html', title="Register", form=form)


#User and owner login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data) and (user.is_owner==False):
            user.is_owner = False
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        elif user and bcrypt.check_password_hash(user.password, form.password.data) and (user.is_owner==True):
            user.is_owner = True
            login_user(user, remember=form.remember.data)
            return redirect(url_for('owner_home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


#User and owner logout
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


#User and owner profile picture
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



#Owner account information
@app.route('/owner_account', methods=['GET', 'POST'])
@login_required
def owner_account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.avatar = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated.', 'success')
        return redirect(url_for('owner_account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    avatar = url_for('static', filename='profile_pics/' + current_user.avatar)

    return render_template('owner_account.html', title='Account', avatar=avatar, form=form)


#User hotel reservations
@app.route('/reservations')
@login_required
def reservations():
    return render_template('reservations.html')


#User adds new hotel
@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_hotel():
    form = PostForm()

    if form.validate_on_submit():
        hotel = Hotel(name=form.name.data, city=form.city.data, state=form.state.data,
                      country=form.country.data, rating=form.rating.data, price_cat=form.price_cat.data,
                      content=form.content.data, owner_id=current_user.id)
        db.session.add(hotel)
        db.session.commit()
        flash('Your hotel has been added.', 'success')
        return redirect(url_for('owner_home'))
    return render_template('create_hotel.html', title='Add Hotel',
                           form=form, legend='Add Hotel')


#Get specific hotel by ID
@app.route("/post/<int:hotel_id>")
@login_required
def post(hotel_id):
    user = User.query.all()
    hotel = Hotel.query.get_or_404(hotel_id)

    if current_user.is_owner == True:
        return render_template('owner_post.html', title=hotel.name, hotel=hotel)
    else:
        return render_template('post.html', title=hotel.name, hotel=hotel)


#Update specific hotel
@app.route("/post/<int:hotel_id>/update", methods=['GET', 'POST'])
@login_required
def update_hotel(hotel_id):
    hotel = Hotel.query.get_or_404(hotel_id)
    if hotel.owner_id != current_user.id:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        hotel.name = form.name.data
        hotel.city = form.city.data
        hotel.state = form.state.data
        hotel.country = form.country.data
        hotel.rating = form.rating.data
        hotel.price_cat = form.price_cat.data
        hotel.content = form.content.data
        db.session.commit()
        flash('Your hotel information has been updated', 'success')
        return redirect(url_for('post', hotel_id=hotel.id))
    elif request.method == 'GET':
        #Populate form with existing data
        form.name.data = hotel.name
        form.city.data = hotel.city
        form.state.data = hotel.state
        form.country.data = hotel.country
        form.rating.data = hotel.rating
        form.price_cat.data = hotel.price_cat
        form.content.data = hotel.content
    return render_template('create_hotel.html', title='Update Hotel',
                       form=form, legend='Update Hotel')


#Update specific hotel
@app.route("/post/<int:hotel_id>/delete", methods=['POST'])
@login_required
def delete_hotel(hotel_id):
    hotel = Hotel.query.get_or_404(hotel_id)
    if hotel.owner_id != current_user.id:
        abort(403)
    db.session.delete(hotel)
    db.session.commit()
    flash('Your hotel has been deleted.', 'success')
    return redirect(url_for('owner_home'))

#User adds new reservation
@app.route("/create_reservation", methods=['GET', 'POST'])
@login_required
def new_reservation():
    form = ReservationForm()

    if form.validate_on_submit():
        reservation = Reservation(date_made=form.date_made.data, user_id=current_user.id)
        db.session.add(reservation)
        db.session.commit()
        flash('Your reservation has been made.', 'success')
        return redirect(url_for('home'))
    return render_template('create_reservation.html', title='Add Reservation', form=form)
