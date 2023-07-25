import sys
from . import db
from .models import Users, Statuses, Requests, Roles, Vendors, Devices, Comments, \
    Sources, Logs
from flask_login import current_user, login_user, logout_user
from sqlalchemy import or_
from werkzeug.security import check_password_hash, generate_password_hash

class LogService:
    def add_log(self, request_id, note):
        new_log = Logs(request_id=request_id, note=note)
        db.session.add(new_log)
        db.session.commit()

class UserService:
    
    def create_new_user(self, username, password, role):
        print(role)
        new_user = Users(username=username, role_id=role)
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
    
    def get_role(self, id):
        Roles.query.get(int(id)) 
    
    def get_all_users(self):
        return Users.query.all()
    
class RequestService:

    def __init__(self):
        self.logging = LogService()
    
    def create_new_request(self, address, name, phone, source, coordinates, author_id):
        new_request = Requests(address=address, 
                            name=name, 
                            phone=phone,
                            source_id=source, 
                            coordinates=coordinates, 
                            author_id=author_id)
        db.session.add(new_request)
        db.session.commit()
        self.logging.add_log(int(new_request.id), f'Заявка {int(new_request.id)} создана пользователем {current_user.username}')
        return 
    
    def get_request(self, request_id):
        return Requests.query.get(int(request_id))
    
    def delete_request(self, request_id):
        request = Requests.query.get(int(request_id))
        db.session.delete(request)
        db.session.commit()
        self.logging.add_log(request.id, f'Заявка {request_id} удалена пользователем {current_user.username}')
    
    def get_all(self):
        return Requests.query.all()
    
    def set_request_status(self, request_id, status_id):
        request = Requests.query.get(int(request_id))
        request.status_id=int(status_id)
        db.session.commit()

    def get_request_dataset(self, address, name, phone, source, base, \
                            device, status, start_date, end_date):
        
        request_dataset = Requests.query \
            .filter(Requests.name.ilike(f'%{name}%'),
                                                Requests.address.ilike(f'%{address}%'),
                                                Requests.phone.ilike(f'%{phone}%'),
                                                Requests.base.ilike(f'%{base}%'))
        if source != '__None':
            request_dataset = request_dataset.filter(Requests.source_id == source)

        if status != '__None':
            request_dataset = request_dataset.filter(Requests.status_id == status)

        if device != '__None':
            request_dataset = request_dataset.filter(Requests.device_id == device)
        
        if start_date and end_date:
            request_dataset = request_dataset.filter(Requests.timestap >= start_date, Requests.timestap <= end_date)
        
        return request_dataset.all()

    def edit_request(self, request_id, form):
        current_request = Requests.query.get(int(request_id))
        current_request.address = form.address.data 
        current_request.name = form.name.data
        current_request.phone = form.phone.data 
        current_request.source_id = form.source.raw_data[0]
        current_request.base = form.base.data
        current_request.device = form.device.data
        current_request.auth_type = form.auth_type.data
        current_request.coordinates = form.coordinates.data
        current_request.status_id = form.status.raw_data[0]
        db.session.commit()
        self.logging.add_log(current_request.id, f'Заявка {request_id} изменена пользователем {current_user.username}')

        

    
    
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
        
    def delete_status(self, id):
        status = Statuses.query.get(int(id)) 
        db.session.delete(status)
        db.session.commit()

class DeviceService:
        
        def get_all_vendors(self):
            return Vendors.query.all()
        
        def get_all_devices(self):
            return Devices.query.all()
        
        def add_vendor(self, name):
            new_vendor = Vendors(name=name)
            db.session.add(new_vendor)
            db.session.commit()
            
        def delete_vendor(self, id):
            vendor = Vendors.query.get(int(id)) 
            db.session.delete(vendor)
            db.session.commit()
            
        def add_device(self, name, vendor):
            new_device = Devices(name=name, vendor_id=vendor)
            db.session.add(new_device)
            db.session.commit()
            
        def delete_device(self, id):
            device = Devices.query.get(int(id)) 
            db.session.delete(device)
            db.session.commit()
        
class CommentService:
    def add_comment(self, request_id, author_id, text):
        comment = Comments(text=text,
                           author_id=author_id,
                           request_id=request_id)
        db.session.add(comment)
        db.session.commit()

class SourceService:
    def get_all_sources(self):
            return Sources.query.all()
    
    def add_source(self, name):
            new_source = Sources(name=name)
            db.session.add(new_source)
            db.session.commit()

    def delete_source(self, id):
            source = Sources.query.get(int(id)) 
            db.session.delete(source)
            db.session.commit()
    

def save():
    db.session.commit()