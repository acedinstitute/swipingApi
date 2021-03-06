from flask import Blueprint, request
from bson.json_util import dumps
from .connection import client

users_route = Blueprint('users_route', __name__)
# setup connection
db = client.swiper
collection = db.binary
users = db.users


@users_route.route('/', methods=['GET'])
def topUsers():
    if request.method == 'GET':
        topTen = collection.aggregate([
            # Do lookup to connect userIds
            {
                '$lookup': {
                    'from': 'users',
                    'localField': 'userId',
                    'foreignField': 'userId',
                    'as': 'user'
                }
            },
            {
                '$group': {  # Group them together based on userId
                    '_id': '$userId',
                    # It returns an array so get first element
                    'username': {'$first': {'$arrayElemAt': ['$user.username', 0]}},
                    #                     'name': users.find( { 'userId': '$userId' }, { username: 1, _id: 0 } ),
                    'count': {'$sum': 1}  # count per user
                }
            },
            {'$sort': {'count': -1}},  # return them descending
            {'$limit': 10}
        ])

        return dumps(topTen), 201
