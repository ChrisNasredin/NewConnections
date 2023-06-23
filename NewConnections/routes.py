from . import app
from .views import IndexView, NewRequestView, LoginView, LogoutView, CreateNewUserView, \
    AdminView, RequestView, DeleteRequestView, EditRequestView, AdminViewDeviceDelete, \
    AdminViewStatusDelete, AdminViewVendorDelete

app.add_url_rule('/', view_func=IndexView.as_view('index'))
app.add_url_rule('/new', view_func=NewRequestView.as_view('new'))
app.add_url_rule('/login', view_func=LoginView.as_view('login'))
app.add_url_rule('/logout', view_func=LogoutView.as_view('logout'))
app.add_url_rule('/admin/create_user', view_func=CreateNewUserView.as_view('create_user'))
app.add_url_rule('/admin', view_func=AdminView.as_view('admin_panel'))
app.add_url_rule('/admin/status/delete', view_func=AdminViewStatusDelete.as_view('delete_status'))
app.add_url_rule('/admin/vendor/delete', view_func=AdminViewVendorDelete.as_view('delete_vendor'))
app.add_url_rule('/admin/device/delete', view_func=AdminViewDeviceDelete.as_view('delete_device'))
app.add_url_rule('/request/<request_id>', view_func=RequestView.as_view('request_item'))
app.add_url_rule('/request/delete/<request_id>', view_func=DeleteRequestView.as_view('delete_request'))
app.add_url_rule('/request/edit/<request_id>', view_func=EditRequestView.as_view('edit_request'))