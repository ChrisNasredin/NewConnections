from . import db
from .models import Users, Statuses, Requests


def create_new_user(username, password, role):
    new_user = Users(username=username, role=role)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    
def get_statuses():
    return Statuses.query.all()

def add_status(status_name):
    new_status = Statuses(status_desc=status_name)
    db.session.add(new_status)
    db.session.commit()
    
    

def user_autentification(username, password):
    user = Users.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user
    else:
        return False
    
def get_dataset():
    return Requests.query.all()

def create_new_request(address, name, phone, coordinates, author_id):
    new_request = Requests(address=address, 
                           name=name, 
                           phone=phone, 
                           coordinates=coordinates, 
                           author_id=author_id)
    db.session.add(new_request)
    db.session.commit()