from app import app
from unittest import TestCase

import json

class TestAPI(TestCase):
	def setUp(self):
		self.app = app.test_client()

	def test_song_list(self):
		response = self.app.get('/songs')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.content_type, 'application/json')
		self.assertGreater(json.loads(response.data).__len__(), 1)

	def test_song_avg_diff(self):
		response = self.app.get('/songs/avg/difficulty?level=3')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.content_type, 'application/json')
		self.assertEqual(json.loads(response.data).__len__(), 1)

	def test_song_search(self):
		response = self.app.get('/songs/search?message=tHe%20yOuSiCiAn')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.content_type, 'application/json')
		self.assertGreater(json.loads(response.data).__len__(), 1)

	def test_song_rating(self):
		response = self.app.post('/songs/rating', data={'song_id':'599f5b281e6d956381505bb4', 'rating': '5'})
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.content_type, 'application/json')
		self.assertEqual(json.loads(response.data)['updated'], True)

	def test_song_avg_rating(self):
		response = self.app.get('/songs/avg/rating/599f5b281e6d956381505bb4')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.content_type, 'application/json')
		self.assertEqual(json.loads(response.data).__len__(), 3)