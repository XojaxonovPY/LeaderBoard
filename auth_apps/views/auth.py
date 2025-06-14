from django.utils.timezone import now
from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from auth_apps.serializer import RegisterModelSerializer


@extend_schema(tags=['auth'])
class RegisterCreateAPIView(CreateAPIView):
    serializer_class = RegisterModelSerializer
    permission_classes = [AllowAny]


@extend_schema(tags=['auth'])
class CustomerTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        # Agar login muvaffaqiyatli bo‘lsa
        if response.status_code == 200:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.user
            user.last_login = now()
            user.save(update_fields=["last_login"])

        return response


@extend_schema(tags=['auth'])
class CustomerTokenRefreshView(TokenRefreshView):
    pass
