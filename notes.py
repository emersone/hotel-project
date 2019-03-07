
            <h2><a class="article-title" href="{{ url_for('post', hotel_id=hotel.id) }}">{{ hotel.name }}</a></h2>
            <h3>{{ hotel.city }}, {{ hotel.state }}, {{ hotel.country }}</h3>


                    <h3 class="article-title">You are reserving a room at {{ hotel.name }} in {{ hotel. city }}, {{ hotel.state }}, {{ hotel.country }}.</h3><br>



#User adds new reservation
@app.route("/create_reservation", methods=['GET', 'POST'])
@login_required
def new_reservation():
    form = ReservationForm()

    if form.validate_on_submit():
        reservation = Reservation(check_in=form.check_in.data, check_out=form.check_out.data, date_made=form.date_made.data, user_id=current_user.id)
        db.session.add(reservation)
        db.session.commit()
        flash('Your reservation has been made.', 'success')
        return redirect(url_for('home'))
    return render_template('create_reservation.html', title='Add Reservation', form=form)





#Reserve specific hotel
@app.route("/post/<int:hotel_id>/reserve", methods=['GET', 'POST'])
@login_required
def update_hotel(hotel_id):
    hotel = Hotel.query.get_or_404(hotel_id)
    if hotel.owner_id == current_user.id:
        abort(403)
    form = ReservationForm()
    if form.validate_on_submit():
        hotel.name = form.name.data
        hotel.city = form.city.data
        hotel.state = form.state.data
        hotel.country = form.country.data
        hotel.rating = form.rating.data
        hotel.price_cat = form.price_cat.data
        hotel.price_night = form.price_night.data
        hotel.content = form.content.data
        db.session.commit()
        flash('Your reservation has been made', 'success')
        return redirect(url_for('post', hotel_id=hotel.id))

    elif request.method == 'GET':
        #Populate form with existing data
        form.name.data = hotel.name
        form.city.data = hotel.city
        form.state.data = hotel.state
        form.country.data = hotel.country
        form.rating.data = hotel.rating
        form.price_cat.data = hotel.price_cat
        form.price_night.data = hotel.price_night
        form.content.data = hotel.content
    return render_template('create_hotel.html', title='Update Hotel',
                       form=form, legend='Update Hotel')



    #Get specific reservation by ID
    @app.route("/reservation/<int:reservation_id>")
    @login_required
    def get_reservation(reservation_id):
        reserve = Reservation.query.get_or_404(id)
        if reserve.user_id != current_user.id:
            abort(403)

        reservations = db.session.query(Reservation).join(User, Reservation.owner_id==User.id).join(Hotel, Reservation.hotel_info==Hotel.id)
        return render_template('create_reservation.html', title=hotel.name, reservations=reservations)





#    HTML:
    #            <img class="img-rounded" src="{{ pic_1 }}">
#                <img class="img-rounded" src="{{ pic_2 }}">
#                <img class="img-rounded" src="{{ pic_3 }}">




#  <h3 class="article-title">You are reserving a room at {{ hotel.name }} in {{ home. city }}, {{ home.state }}, {{ home.country }}.





            <div class="form-group">
                <p>{{ form.pic_1.label(class="form-control-label") }} <input type="file" name="pic_1" id="pic_1" accept="image/*"></p>
                {% if form.pic_1.errors %}
                      {% for error in form.pic_1.errors %}
                          <span class="text-danger">{{ error }}</span><br>
                        {% endfor %}
                  {% endif %}
                <p>{{ form.pic_2.label() }} <input type="file" name="pic" accept="image/*"></p>
                {% if form.pic_2.errors %}
                      {% for error in form.pic_2.errors %}
                          <span class="text-danger">{{ error }}</span><br>
                        {% endfor %}
                  {% endif %}
                <p>{{ form.pic_3.label() }} <input type="file" name="pic" accept="image/*"></p>
                {% if form.pic_3.errors %}
                      {% for error in form.pic_3.errors %}
                          <span class="text-danger">{{ error }}</span><br>
                        {% endfor %}
                  {% endif %}
          </div>


            <img class="img-rounded" src="{{ pic_1 }}"></p>
