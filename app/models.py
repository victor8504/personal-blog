from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Permission:
    FOLLOW = '0*01'
    COMMENT = '0*02'
    WRITE_ARTICLES = '0*04'
    MODERATE_COMMENTS = '0*08'
    ADMINISTER = '0*80'

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True)
    default = db.Column(db.Boolean, default = False, index = True)
    permissions = db.Column(db.Integer)

    users = db.relationship('User', backref = 'role', lazy = 'dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.FOLLOW |
                     Permission.COMMENT |
                     Permission.WRITE_ARTICLES, True),
            'Moderator': (Permission.FOLLOW |
                          Permission.COMMENT |
                          Permission.WRITE_ARTICLES |
                          Permission.MODERATE_COMMENTS, False),
            'Administrator': (0*ff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name = r).first()
            if role is None:
                role = Role(name = r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
            db.session.commit()

    def __repr__(self):
        return f'User {self.name}'

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

    
    confirmed = db.Column(db.Boolean, default=False)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)

        except:
            return False

        if data.get('confirm') != self.id:
            return False

        self.confirmed = True
        db.session.add(self)
        return True

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))    

    blogs = db.relationship("Blog", backref = "user", lazy = "dynamic")

    comments = db.relationship("Comment", backref = "user", lazy = "dynamic")

    # Method to give the models a readable string representation to facilitate debugging and testing
    def __repr__(self):
        return f'User {self.username}'


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
    
