from flask_restful import reqparse, abort, Api, Resource, fields, marshal_with

BD = {
    'id1': {'id': 1, 'username': 'Mayue', 'email':"myyue@gmail.com"},
    'id2': {'id': 2, 'username': 'Wangxiao', 'email': "wangxiao@gmail.com"},
    'id3': {'id': 3, 'username': 'Dingpeng', 'email': "dingpeng@gmail.com"},
    'id4': {'id': 4, 'username': 'Yangguo', 'email': "yangguo@gmail.com"},
}

def email(email_str):
    print('email_str==', email_str)
    return email_str
    """ return True if email_str is a valid email """
    # if valid_email(email):
    #     return True
    # else:
    #     raise ValidationError("{} is not a valid email")


req_parser = reqparse.RequestParser()
req_parser.add_argument(
    'username', dest='username',
    type=str,
    required=True, help='The user\'s username',
)
req_parser.add_argument(
    'email', dest='email',
    type=email,
    required=True, help='The user\'s email',
)
# req_parser.add_argument(
#     'user_priority', dest='user_priority',
#     type=int,
#     default=1, choices=range(5), help='The user\'s priority',
# )

user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'email': fields.String,
    # 'user_priority': fields.Integer,
    # 'custom_greeting': fields.FormattedString('Hey there {username}!'),
    # 'date_created': fields.DateTime,
    # 'date_updated': fields.DateTime,
    # 'links': fields.Nested({
    #     'friends': fields.Url('/Users/{id}/Friends'),
    #     'posts': fields.Url('Users/{id}/Posts'),
    # }),
}


class User(Resource):

    @marshal_with(user_fields)
    def post(self):
        pass
        # args = req_parser.parse_args()
        # user = create_user(args.username, args.email, args.user_priority)
        # return user

    @marshal_with(user_fields)
    def get(self,id):
        print('id==', id)
        print('req_parser==', req_parser.parse_args())
        # args = get_parser.parse_args()
        # user = fetch_user(id)
        # return BD
        return BD['id'+id]
