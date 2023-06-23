from .import db
from NewConnections import login
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), info={'label': 'Имя Пользователя'})
    password_hash = db.Column(db.String(256))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), info={'label': 'Роль'})
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
    name = db.Column(db.String(256))
    users = db.relationship('Users', backref='role', lazy='dynamic')
    
    def __repr__(self):
        return self.name
    
class Statuses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status_desc = db.Column(db.String(256))
    requests = db.relationship('Requests', backref='status', lazy='dynamic')
        
    
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
    connection_type = db.Column(db.String(256), index=True, nullable=True)
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'), nullable=True)
    base = db.Column(db.String(256), index=True, nullable=True)
    auth_type = db.Column(db.String(256), index=True, nullable=True)
    comments = db.relationship('Comments', backref='request', lazy='dynamic')
    source_id = db.Column(db.Integer, db.ForeignKey('sources.id'), nullable=True)

class Devices(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'))
    name = db.Column(db.String(256), index=True)
    
class Vendors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), index=True)
    devices = db.relationship('Devices', backref='vendor', lazy='dynamic')
    
    def __repr__(self):
        return self.name
    
class Sources(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), index=True)
    requests = db.relationship('Requests', backref='status', lazy='dynamic')
    
    
class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime, default=datetime.now)
    request_id = db.Column(db.Integer, db.ForeignKey('requests.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))