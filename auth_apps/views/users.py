from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from auth_apps.models import User
from auth_apps.serializer import StudentListSerializer, UserProfileSerializer


@extend_schema(tags=['User'])
class StudentsListAPIView(ListAPIView):
    serializer_class = StudentListSerializer

    def get_queryset(self):
        queryset = User.objects.filter(role='student')
        course_id = self.request.query_params.get('course_id')
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response({
            "status": 200,
            "students": serializer.data
        })


@extend_schema(tags=['User'])
class UserProfileAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'pk'


