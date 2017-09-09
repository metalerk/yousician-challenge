from flask_restful import Resource
from flask_restful import reqparse
from flask import jsonify
from flask import request
from flask_pymongo import pymongo
from bson.objectid import ObjectId
from api.utils.api_utils import objectid_to_str

from math import ceil

class SongList(Resource):

    def __init__(self, db, parser):
        self.db = db
        self.qs = self.db.songs.find({})
        self.page = None
        self.per_page = None
        self.pages = None
        self.parser = parser

    def get(self):

        args = self.parser.parse_args()

        if args['page'] is not None:

            self.page = args['page'] if args['page'] > 1 else 1
            
            self.per_page = args['per_page'] if (args['per_page'] is not None and args['per_page'] > 1) else 4

            response = {
                'current_page': self.page,
                'total_pages': self.pages,
                'songs_per_page': self.per_page,
                'songs' : [objectid_to_str(song) for song in self.queryset_pagination]
            } if self.queryset_pagination is not None else {
                'error': 'Page not found'
            }

        else:

            response = {
                'total': self.qs.count(),
                'songs' : [objectid_to_str(song) for song in self.qs]
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

    def __init__(self, db, parser):
        self.db = db
        self.level = None
        self.qs = self.db.songs
        self.parser = parser

    def get(self):

        args = self.parser.parse_args()

        self.level = args['level']

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

        return ceil(list(self.qs)[0]['avg_diff'])

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

        return ceil(res_qs[0]['avg_diff']) if res_qs else 0

class SongSearch(Resource):

    def __init__(self, db, parser):
        self.db = db
        self.qs = self.db.songs
        self.message = None
        self.parser = parser

    def get(self):

        args = self.parser.parse_args()

        self.message = args['message']

        if self.message is not None:

            return jsonify({
                'songs': self.search_queryset,
                'total': self.search_queryset.__len__()
            })

        else:

            return jsonify({
                'error': 'You must provide a search string',
                'missing_parameter': 'message'
            })

    @property
    def search_queryset(self):
        rqs = self.qs.find({ 
            '$or': [
                    {'artist': {'$regex': r'(?i){}'.format(self.message) }}, 
                    {'title': {'$regex': r'(?i){}'.format(self.message) }} 
            ]})

        return [objectid_to_str(song) for song in rqs] if rqs else []

class SongRating(Resource):

    def __init__(self, db, parser):
        self.db = db
        self.qs = self.db.songs
        self.parser = parser

    def post(self):

        args = self.parser.parse_args()

        if args['song_id'] is not None and (args['rating'] in range(1, 6) and args['song_id'].__len__() == 24):
            if self.rate_song(args['song_id'], args['rating']):
                return jsonify({
                        'updated': True
                    })

            else:
                return jsonify({
                        'updated': False
                    })

        else:
            return jsonify({
                    'error': 'Bad parameters'
                })            

    def rate_song(self, song_id, rating):
        song = self.qs.find_one({"_id": ObjectId(song_id)})

        if song:
            
            if not 'rating' in song:
                song['rating'] = list()
                song['rating'].append(rating)

            else:
                song['rating'].append(rating)

            self.qs.save(song)

            return True

        else:
            return False

class SongAverage(Resource):
    def __init__(self, db):
        self.db = db
        self.qs = self.db.songs

    def get(self, song_id):

        if song_id.__len__() == 24:
            avg_max_min = self.get_average(song_id)

            if avg_max_min:

                return jsonify({
                    'average_rating': ceil(avg_max_min['avg']),
                    'max_rating': avg_max_min['max'],
                    'min_rating': avg_max_min['min'],
                })

            else:

                return jsonify({
                        'error': 'song not found'
                    })

        return jsonify({
                        'error': 'song_id must be 24 characters'
                    })

    def get_average(self, song_id):
        rqs = self.qs.aggregate([
                { '$match': 
                    {'_id': ObjectId(song_id)}
                }, 
                {'$project': 
                    { '_id': 0, 'avg': { '$avg': '$rating'}, 'min': {'$min' : '$rating'}, 'max': {'$max' : '$rating'}}
                }
            ])

        res = list(rqs)

        if res.__len__() >= 1:
            res = res[0]
            for key, val in res.items():
                if val == None:
                    res[key] = 0

            return res

        else:
            return []