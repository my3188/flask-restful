import random
from test import __variableMayue, mayuefun
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource, fields, marshal_with

print('variableMayue==>', __variableMayue)
mayuefun()

app = Flask(__name__)
api = Api(app)



TODOS = {
    'todo1': {'task': '第1条任务'},
    'todo2': {'task': '第二条任务',"name":'马越','id':88},
    'todo3': {'task': '第3条任务'},
}



class UnreadItem(fields.Raw):
    def format(self, value):
        return "Unread" if value else "Read"


class RandomNumber(fields.Raw):
    def output(self, key, obj):
        return random.random()
# print('fields', dir(fields))
resource_fields = {
    'random': RandomNumber,
    'uri': fields.Url(absolute=True),
    'status': UnreadItem(attribute='task'),
    'outter_task': fields.String(attribute='task', default='Anonymous task'),
    # 'info':fields
    # 'address': fields.String,
    # 'date_updated': fields.DateTime(dt_format='rfc822'),
}

def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))

parser = reqparse.RequestParser()

parser.add_argument('task', type=str,  help='task must is str')
parser.add_argument('money', type=int,  help='money must is str')
parser.add_argument('name', type=str, default='MaYue',
                    help='name must is str')
parser.add_argument('age', type=int, action='append',
                    help='age must is int', dest='py_age')
parser.add_argument('info', type=str, action='store',
                    help='info must is int')

# Todo
#   show a single todo item and lets you delete them
class Todo(Resource):
    @marshal_with(resource_fields, envelope='singleData')
    def get(self, todo_id):
        args = parser.parse_args()
        print('args-->', args)
        print('todo_id==',todo_id)
        abort_if_todo_doesnt_exist(todo_id)
        return TODOS[todo_id]

    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return '', 204

    def put(self, todo_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        TODOS[todo_id] = task
        return task, 201


# TodoList
#   shows a list of all todos, and lets you POST to add new tasks
class TodoList(Resource):
    
    def get(self):
        return TODOS

    def post(self):
        args = parser.parse_args()
        print('args-->',args)
        print('args-->',type(args))
        todo_id = 'todo%d' % (len(TODOS) + 1)
        TODOS[todo_id] = args
        # TODOS[todo_id] = {'task': args['task']}
        return TODOS[todo_id], 201

##
## Actually setup the Api resource routing here
##
api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<string:todo_id>')


if __name__ == '__main__':
    app.run(debug=True)
