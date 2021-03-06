import math
from flask import request, Blueprint, json
from bson.json_util import dumps
from .connection import client

title_route = Blueprint('title_route', __name__)

# Connection to collection
db = client.swiper
# get collectoins
collectionTitles = db.testTitles
binarySet = db.binary
average = db.average


@title_route.route('/', methods=['GET', 'POST'])
def returnTitles():
    if request.method == 'GET':  # return all
        return 'GET ALL THE THE TITLES', 200
    else:  # check for post with userid and everything
        if 'id' in request.json and request.json['id'] != '':
            id = request.json['id']  # id from the post with userid
            if binarySet.find({'userId': id}).count() > 0:
                titlesSeen = list(binarySet.aggregate([  # the list is to transform the cursor to a list
                    {'$match': {'userId': id}},
                    {'$group':
                        {
                            '_id': 0,
                            'titleKeys': {
                                '$push': '$primary_key'
                            }
                        }
                     }
                ]))[0]['titleKeys']  # get only list of key
                # Get all swipes
                averageData = average.find({})

                for averageData in averageData:
                    if averageData['calculate']:
                        avergageSwipes = math.ceil(db.binary.find({}).count() / db.testTitles.find({}).count())
                    else:
                        avergageSwipes = averageData['staticAverage']
                        pass

                title = getTitle(avergageSwipes, titlesSeen)

            else:
                title = collectionTitles.aggregate([{'$sample': {'size': 1}}, {'$project': {'title': 1, 'description': 1, 'url': 1, 'primary_key': 1, 'og-title': 1, 'timestamp': 1, '_id': 0}}])

            return dumps(title), 200
        else:
            return 'id not filled', 403


def getTitle(avgSwipe, titlesSeen):
    title = collectionTitles.aggregate([  # Get the titles
        {'$match': {'primary_key': {'$nin': titlesSeen}}},
        # {'$match': {'primary_key': 'c6d2b0e632b3ee2d0a3675120db5a143'}}, test case
        {'$sample': {'size': 1}},
        {'$project': {'title': 1, 'description': 1, 'url': 1, 'primary_key': 1, 'timestamp': 1, '_id': 0}},
        {
            '$lookup': {
                'from': "binary",
                'localField': "primary_key",
                'foreignField': "primaryKey",
                'as': "swipeData"
            }
        }
    ])
    # Count the amount the amount of swipes to compare with average
    for title in title:
        print(len(title['swipeData']))
        if len(title['swipeData']) > avgSwipe:
            getTitle(avgSwipe, titlesSeen)
        else:
            return title
