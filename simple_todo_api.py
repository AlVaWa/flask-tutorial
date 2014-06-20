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

	def __init__(self, text=''):
		self.text = text
		self.completed = 0
		self.created = datetime.now()

	def to_dict(self):
		return {
			'id': self.id,
			'text': self.text,
			'completed': self.completed,
			'created': self.created.isoformat()
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


@app.route('/api/todos')
def api_get_todos():
	todos = db.session.query(Todo).all()

	response = flask.make_response()
	response.mimetype = 'application/json'
	response.status_code = 200
	response.data = to_json(todos)

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
