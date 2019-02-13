from flask_sqlalchemy import SQLAlchemy
import random
import os
from flask import Flask, session, request
from flask_restful import reqparse, abort, Api, Resource, fields, marshal_with
from resources.user import User
from resources.system import Login, Logout

# 设置sqlite绝对路径
def setSqlLiteAbsPath():
    basedir = os.path.abspath(os.path.dirname(__file__))  # 获取当前文件的绝对路径
    basedirWithoutDriver = os.path.splitdrive(basedir)[1]  # 去除盘符名称 win下
    sqlUrl = basedirWithoutDriver.replace("\\", '/')  # 将\转换为/
    sqlUrl = sqlUrl.replace('/', '', 1)  # 将第一个/删除
    return 'sqlite:////'+os.path.join(sqlUrl, 'data.db')

# 设置sqlite相对路径
def setSqlLiteRelativePath():
    return 'sqlite:///data.db'


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # 3个斜杆是相对路径
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


app.config['SQLALCHEMY_DATABASE_URI'] = setSqlLiteAbsPath()
# app.config['SQLALCHEMY_DATABASE_URI'] = setSqlLiteRelativePath()



db = SQLAlchemy(app)

class Users(db.Model):
    # __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username


# db.create_all()

# num = 100
# while num>0:
#     admin = Users('admin'+str(num), 'admin@example.com'+str(num))
#     db.session.add(admin)
#     num = num-1
# admin = Users('admin', 'admin@example.com')
# guest = Users('guest', 'guest@example.com')
# db.session.add(admin)
# db.session.add(guest)
# db.session.commit()
# db.session.close()
usersRS = Users.query.all()
print(usersRS)


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
