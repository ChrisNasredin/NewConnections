from .import db
from .models import Users, Statuses


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