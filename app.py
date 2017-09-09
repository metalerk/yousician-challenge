from flask import Flask
from flask_restful import Resource, Api
from pymongo import MongoClient
from flask import jsonify

from api.songs import SongList

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

api.add_resource(SongList, '/songs', '/songs/<int:page>', '/songs/<int:page>/<int:per_page>', resource_class_kwargs={'db' : db})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)