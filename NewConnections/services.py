import sys
from . import db
from .models import Users, Statuses, Requests, Roles
from flask_login import current_user, login_user, logout_user

class UserService:
    
    def create_new_user(self, username, password, role):
        new_user = Users(username=username, role=role)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
    def user_autentification(self, username, password):
        user = Users.query.filter_by(username=username).first()
        if user and user.check_password(password):
            return user
        else:
            return False
        
    def get_roles(self):
        return Roles.query.all()
    
class RequestService:
    def create_new_request(self, address, name, phone, coordinates, author_id):
        new_request = Requests(address=address, 
                            name=name, 
                            phone=phone, 
                            coordinates=coordinates, 
                            author_id=author_id)
        db.session.add(new_request)
        db.session.commit()
        return 
    
    def get_request(self, request_id):
        return Requests.query.get(int(request_id))
    
    def delete_request(self, request_id):
        request = Requests.query.get(int(request_id))
        db.session.delete(request)
        db.session.commit()
    
    def get_all(self):
        return Requests.query.all()
    
    def set_request_status(self, request_id, status_id):
        request = Requests.query.get(int(request_id))
        request.status_id=int(status_id)
        db.session.commit()
    
class AdminPanel():
    
    category = {
                    'users': None,
                    'statuses': None,
                }

class StatusService:
    
    def get_statuses(self):
        return Statuses.query.all()

    def add_status(self, status_name):
        new_status = Statuses(status_desc=status_name)
        db.session.add(new_status)
        db.session.commit()

        
        
        


def save():
    db.session.commit()