from flask import Flask
from flask_restful import Resource, Api, reqparse
from pymongo import MongoClient

from api.songs import SongList
from api.songs import SongDifficulty
from api.songs import SongSearch
from api.songs import SongRating
from api.songs import SongAverage

import os
import random
import string

app = Flask(__name__)

api = Api(app)

app.config['DEBUG'] = True

app.config['SECRET_KEY'] = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(50))
app.config['MONGO_URI'] = os.environ['MONGO_URI']
app.config['MONGO_DBNAME'] = os.environ['MONGO_DBNAME']

client = MongoClient(app.config['MONGO_URI'])
db = client[app.config['MONGO_DBNAME']]


parser = reqparse.RequestParser()

api.add_resource(SongList, '/songs', resource_class_kwargs={'db' : db, 'parser': parser})
api.add_resource(SongDifficulty, '/songs/avg/difficulty', resource_class_kwargs={'db' : db, 'parser': parser})
api.add_resource(SongSearch, '/songs/search', resource_class_kwargs={'db' : db, 'parser': parser})
api.add_resource(SongRating, '/songs/rating', resource_class_kwargs={'db' : db, 'parser': parser})
api.add_resource(SongAverage, '/songs/avg/rating/<string:song_id>', resource_class_kwargs={'db' : db})


parser.add_argument('page', type=int)
parser.add_argument('per_page', type=int)
parser.add_argument('level', type=int)
parser.add_argument('message', type=str)
parser.add_argument('song_id', type=str, location='form')
parser.add_argument('rating', type=int, location='form')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)