from google.cloud import datastore
from flask import Flask, render_template, current_app, request
import logging

client = datastore.Client()
app = Flask(__name__)

hotel_list = list
kind='Hotel'

#--------------------- Model Functions ---------------------#
def init_app(app):
    pass


def from_datastore(entity):
    entity['id'] = entity.key.id
    return entity


def get_client():
        return datastore.Client(current_app.config['hotelsystem'])


#View hotels
def list_of_hotels(limit=10, cursor=None):
    ds = get_client()

    query = ds.query(kind='Hotel', order=['name'])
    query_iterator = query.fetch(limit=limit, start_cursor=cursor)
    page = next(query_iterator.pages)

    entities = hotel_list(map(from_datastore, page))
    next_cursor = (
        query_iterator.next_page_token.decode('utf-8')
        if query_iterator.next_page_token else None)

    return entities, next_cursor


#--------------------- Controller Functions ---------------------#
@app.route('/home')
def homepage():
    return render_template('home.html')


@app.route('/hotels')
def hotels():
    hotels = [
        {
            'name': "my hotel",
            'num_guests': 5
        }
    ]
    # entities, next_cursor = list_of_hotels()
    return render_template('hotels.html', hotels=hotels)


@app.route('/reservations')
def reservations():
    return render_template('reservations.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
