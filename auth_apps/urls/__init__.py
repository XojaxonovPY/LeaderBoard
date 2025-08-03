from auth_apps.urls.auth import urlpatterns as auth
from auth_apps.urls.admin import urlpatterns as groups

urlpatterns = [
    *auth,
    *groups
]
