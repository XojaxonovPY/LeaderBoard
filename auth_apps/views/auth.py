from django.utils.timezone import now
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from auth_apps.models import User, Sessions


@extend_schema(tags=['auth'])
class CustomerTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        phone=request.data.get('phone')
        user=User.objects.filter(phone=phone).first()
        device={
            'device_name':request.META.get('HTTP_USER_AGENT'),
            'ip_address':request.META.get('REMOTE_ADDR'),
        }
        Sessions.objects.create(user=user,**device)
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
