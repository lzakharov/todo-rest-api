import unittest
from app import create_app, db
from flask import json


class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.item = {'name': 'Make cake'}
        self.base_url = '/todo/api/v1.0/'

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_api_item_creation(self):
        resp = self.client.post(self.base_url + 'items',
                                data=json.dumps(self.item),
                                content_type='application/json')
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(json.loads(resp.data)['name'], self.item['name'])

    def test_api_can_get_all_items(self):
        resp = self.client.post(self.base_url + 'items',
                                data=json.dumps(self.item),
                                content_type='application/json')
        self.assertEqual(resp.status_code, 201)
        resp = self.client.get(self.base_url + 'items')
        self.assertEqual(resp.status_code, 200)
        items = json.loads(resp.data)
        self.assertEqual(items[0]['name'], self.item['name'])

    def test_api_can_delete_item(self):
        resp = self.client.post(self.base_url + 'items',
                                data=json.dumps(self.item),
                                content_type='application/json')
        self.assertEqual(resp.status_code, 201)
        item = json.loads(resp.data)
        resp = self.client.delete(self.base_url +
                                  'items/{}'.format(item['id']))
        self.assertEqual(resp.status_code, 200)
        resp = self.client.get(self.base_url + 'items')
        self.assertEqual(resp.status_code, 200)
        items = json.loads(resp.data)
        self.assertEqual(items, [])
