from .import db
from NewConnections import login
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), info={'label': 'Имя Пользователя'})
    password_hash = db.Column(db.String(256))
    role = db.Column(db.Integer, db.ForeignKey('roles.id'), info={'label': 'Роль'})
    requests = db.relationship('Requests', backref='author', lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
        
    def __repr__(self):
        return f'User {self.username}, role {self.role}'
    
@login.user_loader
def load_user(id):
        return Users.query.get(int(id))   
    
    
    
class Roles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role_desc = db.Column(db.String(256))
    
    @classmethod
    def choice_roles(cls):
        return cls.query.all()
    
    def __repr__(self):
        return self.role_desc
    
class Statuses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status_desc = db.Column(db.String(256))
    requests = db.relationship('Requests', backref='status', lazy='dynamic')
    
    @classmethod
    def get_statuses(cls):
        return cls.query.all()
        
    
    def __repr__(self):
        return self.status_desc
    
    
class Requests(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(256), index=True)
    name = db.Column(db.String(256), index=True)
    coordinates = db.Column(db.String(256), index=True, nullable=True)
    phone = db.Column(db.String(13), index=True)
    timestap = db.Column(db.DateTime, default=datetime.now)
    status_id = db.Column(db.Integer, db.ForeignKey('statuses.id'), default=1)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    
    