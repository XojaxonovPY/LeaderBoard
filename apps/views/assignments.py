from rest_framework.generics import  CreateAPIView, ListAPIView

from apps.models import Assignment
from apps.serializer import AssignmentsSerializer
from auth_apps.permissions import IsTeacher


class AssignmentCreateView(CreateAPIView):
    serializer_class = AssignmentsSerializer
    permission_classes = [IsTeacher]



class StudentAssignmentsListAPIView(ListAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentsSerializer

    def get_queryset(self):
        student=self.request.user
        query=super().get_queryset()
        query=query.filter(course=student.course)
        return query













