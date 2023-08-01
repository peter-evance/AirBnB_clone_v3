#!/usr/bin/python3
"""Index route"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State
from models.user import User
from models.review import Review


clss_obj = {'amenties': Amenity, 'cities': City,
            'places': Place, 'reviews': Review, 'states': State, 'users': User}


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Returns status of API"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """retrieves the number of each objects by type"""

    count_objs = {}
    for obj, clss in clss_obj.items():
        count_objs[obj] = storage.count(clss)

    return jsonify(count_objs)
