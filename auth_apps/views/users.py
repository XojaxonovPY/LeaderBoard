from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from auth_apps.models import User
from auth_apps.serializer import StudentListSerializer, UserProfileSerializer



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


class UserProfileAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'user_id'

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)

            return Response({
                "status": 200,
                "profile": serializer.data
            })
        except User.DoesNotExist:
            return Response({
                "status": 404,
                "message": "Foydalanuvchi topilmadi"
            })


