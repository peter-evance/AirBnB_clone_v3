#!/usr/bin/python3
"""View for Place objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from models.city import City
from models.place import Place
from models.user import User
from models import storage
from flask import jsonify, abort, make_response, request


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    places_list = []
    places = storage.all(Place)
    for place in places.values():
        if place.city_id == city_id:
            places_list.append(place.to_dict())

    return jsonify(places_list)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place_with_id(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ Deletes a Place object """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """ Creates a Place """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400, description='Not a JSON')

    if 'user_id' not in data:
        abort(400, description='Missing user_id')

    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)

    if 'name' not in data:
        abort(400, description='Missing name')
    place = Place(**data)
    storage.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """ Updates a Place object """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, description='Not a JSON')
    static_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, val in data.items():
        if key not in static_keys:
            setattr(place, key, val)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
