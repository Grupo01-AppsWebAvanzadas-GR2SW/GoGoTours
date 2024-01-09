from src.web.views.chat_view import ChatView
from src.web.views.home_view import HomeView
from src.web.views.package_detail_view import PackageDetailView
from src.web.views.package_add_manager import PackageAddView
from web.views.package_edit_manager import PackageEditView
from web.views.package_search_view import PackageSearchView
from web.views.package_delete_view import PackageDeleteView


def register_views(app):
    app.add_url_rule('/chat', view_func=ChatView.as_view('chat'))
    app.add_url_rule('/home', view_func=HomeView.as_view('home'))
    app.add_url_rule('/package_detail/<string:name>', view_func=PackageDetailView.as_view('package_detail'))
    app.add_url_rule('/edit_package/<string:name>', view_func=PackageEditView.as_view('edit_package'))
    app.add_url_rule('/addPackage', view_func=PackageAddView.as_view('add_package'))
    app.add_url_rule('/deletePackage/<string:name>', view_func=PackageDeleteView.as_view('delete_package'))
    app.add_url_rule('/package_search', view_func=PackageSearchView.as_view('package_search'))
