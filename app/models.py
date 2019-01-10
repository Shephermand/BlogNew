# 根据数据库编写所有的实体类
# 导入 db 到model.py
from . import db
# 通过db创建实体类


class Blogtype(db.Model):
    __tablename__ = 'blogtype'
    id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String(20), nullable=False)
    topices = db.relationship(
        "Topic",
        backref="blogtype",
        lazy="dynamic"
    )


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    cate_name = db.Column(db.String(50), nullable=False)
    topices = db.relationship(
        "Topic",
        backref="category",
        lazy="dynamic"
    )


class Reply(db.Model):
    __tablename__ = 'reply'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.ID'), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    reply_time = db.Column(db.DateTime)


class Topic(db.Model):
    __tablename__ = 'topic'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False)
    read_num = db.Column(db.Integer, default=0)
    content = db.Column(db.Text, nullable=False)
    images = db.Column(db.Text, nullable=True)
    blogtype_id = db.Column(db.Integer, db.ForeignKey('blogtype.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.ID'))
    replies = db.relationship(
        "Reply",
        backref="topic",
        lazy='dynamic'
    )
    voke_users = db.relationship(
        "User",
        secondary="voke",
        lazy="dynamic",
        backref=db.backref("voke_topices", lazy="dynamic")
    )


class User(db.Model):
    __tablename__ = 'user'
    ID = db.Column(db.Integer, primary_key=True)
    loginname = db.Column(db.String(50), nullable=False)
    uname = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(200))
    upwd = db.Column(db.String(30), nullable=False)
    is_author = db.Column(db.Boolean,default=False)
    replies = db.relationship(
        "Reply",
        backref="user",
        lazy='dynamic'
    )
    topices = db.relationship(
        "Topic",
        backref="user",
        lazy="dynamic"
    )


class Voke(db.Model):
    __tablename__ = 'voke'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.ID'), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=False)




