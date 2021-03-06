from flask import Blueprint, request
from .connection import client
import datetime

now = datetime.datetime.utcnow()

user_route = Blueprint('user_route', __name__)

# Connect to collection
db = client.swiper
collection = db.users

# Post/get route acceser
@user_route.route('/', methods=['GET', 'POST'])
def userCreate():
    if request.method == 'POST':

        # Check if object is complete
        if 'username' in request.json and type(request.json['username']) == str and collection.find({'username': request.json['username']}).count() == 0:
            userObject = request.json
            userObject['strikes'] = 0
            userObject['userId'] = request.json['id']
            userObject['timestamp'] = now.strftime('%Y-%m-%d')

            collection.insert_one(userObject)
            return 'success', 201
        else:
            return 'POST BODY NOT COMPLETE', 400
    else:
        return 'Welcome to the post user'
