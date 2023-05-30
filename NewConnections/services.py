from .import db
from .models import Users


def create_new_user(username, password, role):
    new_user = Users(username=username, role=role)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()