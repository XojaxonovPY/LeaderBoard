from apps.urls.assignments import urlpatterns as assigment
from apps.urls.submissions import urlpatterns as submission

urlpatterns=[
    *assigment,
    *submission
]
