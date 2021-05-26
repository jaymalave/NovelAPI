from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from sqlalchemy.engine import result


db_connect = create_engine('sqlite:///novels.db')
app = Flask(__name__)
api = Api(app)

class Novels(Resource):
	def get(self):
		conn = db_connect.connect()
		query = conn.execute("select * from books")
		result = {'novels': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
		return jsonify(result)

class HomePage(Resource):
	def get(self):
		return "Welcome to the Novels API"

class Novel(Resource):
	def get(self, book_name):
		conn = db_connect.connect()
		query = conn.execute("select NAME, AUTHOR from books where NAME like {0}".format(book_name))
		result = {'result': query}
		return jsonify(result)
		

api.add_resource(HomePage, '/')
api.add_resource(Novels, '/novels')
api.add_resource(Novel, '/<string:book_name>')

if __name__ == '__main__':
	 app.run(debug=True)