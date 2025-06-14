from django.urls import path
from apps.views import AssignmentCreateView,StudentAssignmentsRetrieveView
urlpatterns =[
    path('assignments', AssignmentCreateView.as_view(), name='assignment-create'),
    path('assignments/student/<int:student_id>', StudentAssignmentsRetrieveView.as_view(), name='student-assignment-list'),
]

