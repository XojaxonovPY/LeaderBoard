from users.urls.admin import urlpatterns as admin
from users.urls.auth import urlpatterns as auth
from users.urls.course import urlpatterns as course
from users.urls.group import urlpatterns as group

urlpatterns = [
    *auth,
    *admin,
    *group,
    *course,
]
