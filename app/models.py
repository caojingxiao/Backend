#################################
#model
#我把数据库类名都加了一个s，麻烦您查找替换
#################################


from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from .db import db
# 用户表

class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)  # 用户ID
    username = db.Column(db.String(80), unique=True, nullable=False)  # 用户名
    email = db.Column(db.String(120), unique=True, nullable=False)  # 邮箱
    password_hash = db.Column(db.String(5), nullable=False)  # 密码哈希
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 注册时间


    def set_password(self, password):
        """ 设置密码的哈希值 """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """ 检查密码是否匹配 """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<Users(id={self.id}, username={self.username}, email={self.email})>"
    
    @classmethod
    def get_user_by_email(cls, email):
        user = cls.query.filter_by(email=email).first()
        return user

    @classmethod
    def login(cls, email, password):
        """ 根据邮箱和密码验证登录 """
        user = cls.query.filter_by(email=email).first()
        if user and user.check_password(password):
            return user
        return None


# 问题表
class Questions(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)  # 问题ID
    title = db.Column(db.String(255), nullable=False)  # 问题标题
    body = db.Column(db.Text, nullable=False)  # 问题内容
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 提问时间
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 提问者的ID

    # 通过关系与用户表关联
    author = db.relationship('Users', backref=db.backref('questions', lazy=True))

    # 与回答表的关系：一个问题可以有多个回答
    answers = db.relationship('Answers', backref='questions', lazy=True)

    def __repr__(self):
        return f"<Questions(id={self.id}, title={self.title}, created_at={self.created_at})>"


# 回答表
class Answers(db.Model):
    __tablename__ = 'answers'

    id = db.Column(db.Integer, primary_key=True)  # 回答ID
    body = db.Column(db.Text, nullable=False)  # 回答内容
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 回答时间
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)  # 所属问题ID
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 回答者的ID

    # 通过关系与用户表关联
    author = db.relationship('Users', backref=db.backref('answers', lazy=True))

    def __repr__(self):
        return f"<Answers(id={self.id}, question_id={self.question_id}, created_at={self.created_at})>"