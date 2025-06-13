from django.urls import path
from apps.views import AssignmentCreateView

urlpatterns = [
    path('assignments', AssignmentCreateView.as_view(), name='assignment-create'),
]
