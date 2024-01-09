from src.web.views.chat_view import ChatView
from src.web.views.home_view import HomeView
from src.web.views.package_detail_view import PackageDetailView
from src.web.views.package_manager import PackageAddView


def register_views(app):
    app.add_url_rule('/chat', view_func=ChatView.as_view('chat'))
    app.add_url_rule('/home', view_func=HomeView.as_view('home'))
    app.add_url_rule('/package_detail/<string:name>', view_func=PackageDetailView.as_view('package_detail'))
    app.add_url_rule('/edit_package/<string:name>', view_func=PackageEditView.as_view('edit_package'))
    app.add_url_rule('/addPackage', view_func=PackageAddView.as_view('add_package'))
    # app.add_url_rule('/package_search/<string:destination_place>', view_func=PackageSearchView.as_view('package_search'))
    app.add_url_rule('/package_search', view_func=PackageSearchView.as_view('package_search'))

