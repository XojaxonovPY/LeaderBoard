from django.urls import path
from apps.views import AssignmentCreateView
from apps.views import StudentAssignmentsListView
urlpatterns = {
    path('assignments', AssignmentCreateView.as_view(), name='assignment-create'),
    path('assignments/student/<int:student_id>', StudentAssignmentsListView.as_view(), name='student-assignment-list'),

}
