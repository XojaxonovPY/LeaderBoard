
from apps.urls.submissions import urlpatterns as submission
from apps.urls.teachers import urlpatterns as teacher

urlpatterns=[
    *submission,
    *teacher
]
