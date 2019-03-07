from flask_sqlalchemy import SQLAlchemy
import random
import os
from datetime import datetime
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
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username


# 内容
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    body = db.Column(db.Text)
    pub_date = db.Column(db.DateTime)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category',
                               backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, title, body, category, pub_date=None):
        self.title = title
        self.body = body
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date
        self.category = category

    def __repr__(self):
        return '<Post %r>' % self.title

# 类别
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %r>' % self.name


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    
    # email = db.relationship('EmailAddress', backref='person',
    #                             lazy='dynamic')

    def __init__(self, name):
        self.name = name
        # self.email = email


class EmailAddress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))

    person = db.relationship(
        'Person', backref=db.backref('emails', lazy='dynamic'))

    def __init__(self, email,person):
        self.email = email
        self.person = person

class Role(db.Model):
  
    __tablename__ = "roles"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(16),unique=True)
    # 给Role类创建一个uses属性，关联users表。
    # backref是反向的给User类创建一个role属性，关联roles表。这是flask特殊的属性。
    # users = db.relationship('User',backref="role")
    # 相当于__str__方法。
    def __repr__(self):
        return "Role: %s %s" % (self.id,self.name)


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
