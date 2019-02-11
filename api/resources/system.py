from flask import  session
from flask_restful import reqparse, abort, Api, Resource, fields, marshal_with

BD = {
    'id1': {'id': 1, 'username': 'Mayue', 'password':"123456"},
    'id2': {'id': 2, 'username': 'Wangxiao', 'password': "123456"},
    'id3': {'id': 3, 'username': 'Dingpeng', 'password': "123456"},
    'id4': {'id': 4, 'username': 'Yangguo', 'password': "123456"},
}

req_parser = reqparse.RequestParser()
req_parser.add_argument(
    'username', dest='username',
    type=str,
    required=True, help='The user\'s username',
)
req_parser.add_argument(
    'password', dest='password',
    type=str,
    required=True, help='The user\'s password',
)


user_fields = {
    'id': fields.Integer,
    'username': fields.String,
}



def checkUser (userName,passWord):
    result = False
    id = -1
    for k,v in BD.items():
        if v['username'] == userName and v['password'] == passWord:
            result = True
            id = k
    if result:
        session['username'] = userName
        return result, id
    else:
        abort(404, message="用户不存在 或者密码错误")

        
class LoginResponse(object):
    def __init__(self, id):
        self.username = BD[id]['username']
        self.id = BD[id]['id']
        # This field will not be sent in the response
        self.msg = '成功'

class Login(Resource):
    @marshal_with(user_fields, envelope='data')
    def post(self):
        args = req_parser.parse_args()
        rs, id = checkUser(args.username, args.password)
        if rs:
            # return BD[id], 201
            return LoginResponse(id), 201

class Logout(Resource):
    # @marshal_with(user_fields)
    def post(self):
        session.pop('username', None)
        # args = req_parser.parse_args()
        # user = create_user(args.username, args.email, args.user_priority)
        return {'msg':'退出登录成功'}
