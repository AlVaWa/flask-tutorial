import flask
import json
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
import os.path


# create the flask application
app = flask.Flask(__name__)

app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'

# Initialize the SQLAlchemy extension
db = SQLAlchemy(app)


# The todo class
class Todo(db.Model):
	__tablename__ = 'Todo'

	id = db.Column('ID', db.Integer, primary_key=True)
	text = db.Column('Text', db.String)
	completed = db.Column('Completed', db.Boolean, default=False)
	created = db.Column('Created', db.DateTime)
	priority = db.Column('Priority', db.Integer, default=1)

	def __init__(self, text=''):
		self.text = text
		self.completed = 0
		priority = 1
		self.created = datetime.now()

	def to_dict(self):
		return {
			'id': self.id,
			'text': self.text,
			'completed': self.completed,
			'created': self.created.isoformat(),
			'priority': self.priority
		}



if not os.path.isfile('todo.db'):
	app.logger.debug('Create database and add example data')
	db.create_all()

	# insert example data
	db.session.add(Todo(u'Lære meg Python'))
	db.session.add(Todo(u'Lære meg Flask'))
	db.session.commit()


# Create json representation of a single todo or a list of todos
def to_json(todos):
	if type(todos) == list:
		return json.dumps([t.to_dict() for t in todos])
	else:
		return json.dumps(todos.to_dict())


@app.route('/')
def index():
	posts = db.session.query(Todo).all()
	return flask.render_template('todos.html', title="Simple TODO")


@app.route('/api/todos', methods=['GET'])
def api_get_todos():
	todos = db.session.query(Todo).all()

	response = flask.make_response()
	response.mimetype = 'application/json'
	response.status_code = 200
	response.data = to_json(todos)

	return response



@app.route('/api/todos/<id>')
def api_get_todo(id):
	todo = db.session.query(Todo).get(id)

	response = flask.make_response()
	response.mimetype = 'application/json'
	response.status_code = 200
	response.data = to_json(todo)

	return response

@app.route('/api/todos', methods=['POST'])
def api_create_todo():
	payload = flask.request.get_json()
	text = payload.get('text', 'Default text')
	
	todo = Todo(text)
	db.session.add(todo)
	db.session.commit()

	response = flask.make_response()
	response.mimetype = 'application/json'
	response.status_code = 201
	response.data = to_json(todo)

	return response


@app.route('/api/todos/<id>', methods=['DELETE'])
def api_delete_todo(id):
	todo = db.session.query(Todo).get(id)
	db.session.delete(todo)
	db.session.commit()

	response = flask.make_response()
	response.mimetype = 'application/json'
	response.status_code = 200

	return response

@app.route('/api/todos/<id>', methods=['PUT'])
def api_update_todo(id):
	payload = flask.request.get_json()
	
	response = flask.make_response()

	todo = db.session.query(Todo).get(id)
	if todo is None:
		response.status_code = 500
	else:
		text = payload.get('text', todo.text)
		completed = payload.get('completed', todo.completed)
		priority = payload.get('priority', todo.priority)
		todo.text = text
		todo.priority = priority
		todo.completed = completed
		db.session.commit()
		response.status_code = 200
		response.data = to_json(todo)	

	response.mimetype = 'application/json'
	return response



# ===============================================
# GET /api/todos/<id>
# POST /api/todos
# PUT /api/todos
# DELETE /api/todos/<id>
# ===============================================


# start application
if __name__ == '__main__':
	#app.run()
	from werkzeug.serving import run_simple
	run_simple('localhost', 5000, app, use_reloader=True)
