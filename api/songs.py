from flask_restful import Resource
from flask import jsonify
from flask_pymongo import pymongo
from math import ceil

class SongList(Resource):

    def __init__(self, db):
        self.db = db
        self.qs = self.db.songs.find({}, {'_id': 0})
        self.page = None
        self.per_page = None
        self.pages = None

    def get(self, page=None, per_page=2):

        if page is not None:

            self.page = page if page > 1 else 1
            
            self.per_page = per_page if per_page > 1 else 1

            response = {
                'current_page': self.page,
                'total_pages': self.pages,
                'songs_per_page': self.per_page,
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

        total_count = self.qs.count()
        self.pages = int(ceil(total_count / float(self.per_page)))
        start =  (self.page * self.per_page) - self.per_page

        if self.page > self.pages:
            return None
        
        else:
            return self.qs.skip(start).limit(self.per_page)

class SongDifficulty(Resource):

    def __init__(self, db):
        self.db = db
        self.level = None
        self.qs = self.db.songs

    def get(self, level=None):

        self.level = level

        if self.level is not None:
            response = {
                'average_difficulty': self.filtered_avg_diff
            }
        else:
            response = {
                'average_difficulty': self.get_avg_diff
            }

        return jsonify(response)

    @property
    def get_avg_diff(self):

        self.qs = self.qs.aggregate([{
            "$group": {
                "_id": None, 
                "avg_diff": { "$avg": "$difficulty" } 
            } 
        }])

        return int(list(self.qs)[0]['avg_diff'])

    @property
    def filtered_avg_diff(self):

        self.qs = self.qs.aggregate([
            { "$match": {
                "level": self.level
            }},
            {"$group": {
                "_id": None, 
                "avg_diff": { "$avg": "$difficulty"},
            } 
        }])

        res_qs = list(self.qs)

        return int(res_qs[0]['avg_diff']) if res_qs else 0

class SongSearch(Resource):

    def __init__(self, db):
        self.db = db
        self.qs = self.db.songs
        self.message = None

    def get(self, message):

        self.message = message

        return jsonify({
            'songs': self.search_queryset
        })

    @property
    def search_queryset(self):
        self.qs = self.qs.find({ 
            '$or': [
                    {'artist': {'$regex': r'(?i){}'.format(self.message) }}, 
                    {'title': {'$regex': r'(?i){}'.format(self.message) }} 
            ]}, 
            {'_id': 0})

        return list(self.qs) if self.qs else []

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