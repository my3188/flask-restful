from flask_sqlalchemy import SQLAlchemy
from app import db

from datetime import datetime


class User(db.Model):
  
    __tablename__ = 'users'

    id = db.Column(Integer, primary_key=True)
    username = db.Column(String(64), nullable=False, index=True)
    password = db.Column(String(64), nullable=False)
    email = db.Column(String(64), nullable=False, index=True)
    articles = db.relationship('Article', backref='author')
    userinfo = db.relationship('UserInfo', backref='user', uselist=False)

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.username)


class UserInfo(db.Model):

    __tablename__ = 'userinfos'

    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(64))
    qq = db.Column(String(11))
    phone = db.Column(String(11))
    link = db.Column(String(64))
    user_id = db.Column(Integer, ForeignKey('users.id'))


class Article(db.Model):

    __tablename__ = 'articles'

    id = db.Column(Integer, primary_key=True)
    title = db.Column(String(255), nullable=False, index=True)
    content = db.Column(Text)
    user_id = db.Column(Integer, ForeignKey('users.id'))
    cate_id = db.Column(Integer, ForeignKey('categories.id'))
    tags = db.relationship('Tag', secondary='article_tag', backref='articles')

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.title)


class Category(db.Model):

    __tablename__ = 'categories'

    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(64), nullable=False, index=True)
    articles = db.relationship('Article', backref='category')

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.name)


article_tag = Table(
    'article_tag', db.Model.metadata,
    db.Column('article_id', Integer, ForeignKey('articles.id')),
    db.Column('tag_id', Integer, ForeignKey('tags.id'))
)


class Tag(db.Model):

    __tablename__ = 'tags'

    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(64), nullable=False, index=True)

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.name)
