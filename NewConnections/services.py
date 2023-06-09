import sys
from . import db
from .models import Users, Statuses, Requests
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


class CRUD:
    def __init__(self, model) -> None:
        
        self.model = getattr(sys.modules[__name__], model)
        
    def create(self, **kwargs):
        instance = self.model(**kwargs)
        db.session.add()
        db.session.commit()
        return instance
    
    def read(self, id='all', filter=None):
        if id == 'all' and filter == None:
            return self.model.query.all()
        return self.model.query.get(int(id))

    def update(self, instance, field, value):
        instance.field = value
        db.session.commit()
    
    def delete(self, instance): 
        db.session.delete(instance)
        db.session.commit()
        
        
        


def save():
    db.session.commit()