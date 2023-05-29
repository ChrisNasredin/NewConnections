from .import db
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), info={'label': 'Имя Пользователя'})
    password_hash = db.Column(db.String(256))
    role = db.Column(db.Integer, db.ForeignKey('roles.id'), info={'label': 'Роль'})
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'User {self.username}, role {self.role}'
    
    
    
class Roles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role_desc = db.Column(db.String(256))
    
    def __repr__(self):
        return self.role_desc
    
class Statuses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status_desc = db.Column(db.String(256))
    
class Requests(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    addresss = db.Column(db.String(256), index=True)
    coordinates = db.Column(db.String(256), index=True)
    phone = db.Column(db.String(13), index=True)
    timestap = db.Column(db.DateTime, default=datetime.now)
    status_id = db.Column(db.Integer, db.ForeignKey('statuses.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    
    