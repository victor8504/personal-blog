from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True)

    users = db.relationship('User', backref = 'role', lazy = 'dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),unique = True, index = True)
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

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))    

    blogs = db.relationship("Blog", backref = "user", lazy = "dynamic")

    comments = db.relationship("Comment", backref = "user", lazy = "dynamic")

    # Method to give the models a readable string representation to facilitate debugging and testing
    def __repr__(self):
        return '<User %r>' % self.username


class Blog(db.Model):
    __tablename__ = 'blogs'

    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(255))
    content = db.Column(db.String)

    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))

    comments = db.relationship("Comment", backref = "blog", lazy = "dynamic")


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer,primary_key = True)
    content = db.Column(db.String)

    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))

    blog_id = db.Column(db.Integer,db.ForeignKey("blogs.id"))
    
