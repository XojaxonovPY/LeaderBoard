from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from auth_apps.models import User
from auth_apps.serializer import RegisterModelSerializer


@extend_schema(tags=['auth'])
class RegisterCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterModelSerializer


@extend_schema(tags=['auth'])
class CustomerTokenObtainPairView(TokenObtainPairView):
    pass

@extend_schema(tags=['auth'])
class CustomerTokenRefreshView(TokenRefreshView):
    pass
