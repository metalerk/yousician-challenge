from flask_restful import Resource
from flask import jsonify
from flask import request
from flask_pymongo import pymongo
from pprint import pprint
from math import ceil

class SongList(Resource):

    def __init__(self, db):
        self.db = db
        self.qs = self.db.songs.find({}, {'_id': 0})
        self.page = None
        self.per_page = None

    def get(self, page=None, per_page=2):

        if page is not None:

            if page > 1:
                self.page = page
            else:
                self.page = 1

            self.per_page = per_page

            response = {
                'page': self.page,
                'songs' : [song for song in self.queryset_pagination]
            } if self.queryset_pagination is not None else {
                'error': 'Page not found'
            }

        else:

            response = {
                'total': self.qs.count(),
                'songs' : [song for song in self.qs]
            }

        return jsonify(response)

    def head(self):
        
        return {}, 200, {'NUMBER_OF_SONGS': self.qs.count()}

    
    @property
    def queryset_pagination(self):

        total_count = self.qs.count() - 1
        pages = int(ceil(total_count / float(self.per_page)))
        print(pages)
        start =  (self.page * self.per_page) - self.per_page

        if self.page > pages + 1:
            return None
        
        else:
            return self.qs.skip(start).limit(self.per_page)

class SongDifficulty(Resource):

    def get(self):
        return jsonify({
            'ping': 'pong'
        })

    def post(self):
        return jsonify({
            'ping': 'pong'
        })

class SongSearch(Resource):

    def get(self):
        return jsonify({
            'ping': 'pong'
        })

    def post(self):
        return jsonify({
            'ping': 'pong'
        })

class SongRating(Resource):

    def get(self):
        return jsonify({
            'ping': 'pong'
        })

    def post(self):
        return jsonify({
            'ping': 'pong'
        })

class SongAverage(Resource):

    def get(self):
        return jsonify({
            'ping': 'pong'
        })

    def post(self):
        return jsonify({
            'ping': 'pong'
        })