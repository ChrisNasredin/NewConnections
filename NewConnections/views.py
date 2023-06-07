from flask import render_template, redirect, flash, url_for
from flask_login import login_required, current_user
from flask.views import View
from .services import UserService, RequestService, get_dataset
from .forms import RegisterForm, NewRequestForm

class LoginRequiredMixin:
    decorators=[login_required]

class IndexView(LoginRequiredMixin,View):
    
    def dispatch_request(self):
        dataset = get_dataset()
        return render_template('index.html', 
                           title='Главная', 
                           dataset=dataset)
        
class NewView(LoginRequiredMixin, View):
    methods=['GET', 'POST']
    
    def dispatch_request(self):
        form = NewRequestForm()
        request_service = RequestService()
        if form.validate_on_submit():
            request_service.create_new_request(address=form.address.data,
                            name=form.name.data,
                            phone=form.phone.data,
                            coordinates=form.coordinates.data,
                            author_id=current_user.id)
            flash('Заявка успешно создана', 'success')
            return redirect(url_for('index'))
        return render_template('new.html', form=form)