from auth_apps.urls.auth import urlpatterns as auth
from auth_apps.urls.users import urlpatterns as users

urlpatterns=[
    *auth,
    *users
]


