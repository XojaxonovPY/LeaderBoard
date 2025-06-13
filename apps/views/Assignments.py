from rest_framework.views import APIView

from apps.serializer import AssignmentsSerializer


class AssignmentCreateView(APIView):
    serializer_class = AssignmentsSerializer
