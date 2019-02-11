import random
from flask import Flask, session, request
from flask_restful import reqparse, abort, Api, Resource, fields, marshal_with
from resources.user import User
from resources.system import Login, Logout

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@app.before_request
def is_login():
    # print('request.path', request.path)
    
    if request.path == "/login":
        return None
    # if 'username' not in session:
    if not session.get("username"):
        abort(404, message="user don't login")

api = Api(app)


##
## Actually setup the Api resource routing here
##
api.add_resource(User, '/users/<id>')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
# api.add_resource(Todo, '/todos/<string:todo_id>')


if __name__ == '__main__':
    app.run(debug=True)
