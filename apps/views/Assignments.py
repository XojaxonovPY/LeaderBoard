from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.serializer import AssignmentsSerializer


class AssignmentCreateView(APIView):
    serializer_class = AssignmentsSerializer


class StudentAssignmentsRetrieveView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]