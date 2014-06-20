import requests
import json
import unittest

class TodoApiTestCase(unittest.TestCase):
	URL_PREFIX = 'http://localhost:5000/api'

	def test_get_todos(self):
		response = requests.get(self.URL_PREFIX + '/todos')

		self.assertEqual(200, response.status_code)
		self.assertEqual('application/json', response.headers['Content-type'])
		self.assertTrue(len(response.json()) > 0)

		todo = response.json()[0]

		self.assertTrue(todo.has_key('id'))
		self.assertTrue(todo.has_key('text'))
		self.assertTrue(todo.has_key('completed'))
		self.assertTrue(todo.has_key('created'))


	def test_get_todo(self):
		response = requests.get(self.URL_PREFIX + '/todos')
		self.assertEqual(200, response.status_code)
		self.assertTrue(len(response.json()) > 0)

		lookup_todo = response.json()[0]

		response = requests.get(self.URL_PREFIX + '/todos/' + str(lookup_todo['id']))

		self.assertEqual(200, response.status_code)
		self.assertEqual('application/json', response.headers['Content-type'])
		self.assertIsNotNone(response.json())

		todo = response.json()

		self.assertTrue(todo.has_key('id'))
		self.assertEqual(lookup_todo['id'], todo['id'])
		self.assertEqual(lookup_todo['text'], todo['text'])
		self.assertEqual(lookup_todo['completed'], todo['completed'])
		self.assertEqual(lookup_todo['created'], todo['created'])


	def test_create_todo(self):
		payload = {
			'text': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
		}
		response = requests.post(self.URL_PREFIX + '/todos', data=json.dumps(payload), headers={'Content-type': 'application/json'})

		self.assertEqual(201, response.status_code)

		todo = response.json()

		self.assertEqual(payload['text'], todo['text'])
		self.assertEqual(False, todo['completed'])


	def test_update_todo(self):
		payload = {
			'text': 'Lorem Ipsum',
			'completed': False
		}
		response = requests.post(self.URL_PREFIX + '/todos', data=json.dumps(payload), headers={'Content-type': 'application/json'})
		self.assertEqual(201, response.status_code)
		todo_id = response.json()['id']

		payload = {
			'text': ' Finibus bonorum et malorum',
			'completed': True
		}
		response = requests.put(self.URL_PREFIX + '/todos/%s' % (todo_id), data=json.dumps(payload), headers={'Content-type': 'application/json'})
		self.assertEqual(200, response.status_code)

		response = requests.get(self.URL_PREFIX + '/todos/%s' % (todo_id))
		self.assertEqual(200, response.status_code)

		self.assertEqual(payload['text'], response.json()['text'])
		self.assertEqual(payload['completed'], response.json()['completed'])


	def test_delete_todo(self):
		response = requests.get(self.URL_PREFIX + '/todos')
		self.assertEqual(200, response.status_code)

		todos = response.json()
		todo_id = todos[-1]['id']

		response = requests.delete(self.URL_PREFIX + '/todos/%s' % (todo_id))
		self.assertEqual(200, response.status_code)

		response = requests.get(self.URL_PREFIX + '/todos/%s' % (todo_id))
		self.assertEqual(500, response.status_code)



if __name__ == '__main__':
	unittest.main(verbosity=2)
	#unittest.main()
