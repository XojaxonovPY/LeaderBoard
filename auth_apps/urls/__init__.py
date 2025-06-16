from auth_apps.urls.auth import urlpatterns as auth
from auth_apps.urls.users import urlpatterns as users
from auth_apps.urls.group import urlpatterns as groups

urlpatterns = [
    *auth,
    *users,
    *groups
]
