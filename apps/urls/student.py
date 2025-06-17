from django.urls import path
from apps.views import SubmissionCreatAPIView

urlpatterns = [
    path('save/submissions', SubmissionCreatAPIView.as_view(), name='submission-save')
]
