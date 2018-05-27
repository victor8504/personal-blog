from . import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    email = db.Column(db.String(255),unique = True, index = True)

    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    blog = db.relationship("Blog", backref = "user", lazy = "dynamic")

    comment = db.relationship("Comment", backref = "user", lazy = "dynamic")


class Blog(db.Model):
    __tablename__ = 'blogs'

    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(255))
    content = db.Column(db.String)

    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))

    comment = db.relationship("Comment", backref = "blog", lazy = "dynamic")


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer,primary_key = True)
    content = db.Column(db.String)

    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))

    blog_id = db.Column(db.Integer,db.ForeignKey("blogs.id"))
    
