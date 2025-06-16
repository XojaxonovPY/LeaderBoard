from django.urls import path
from rest_framework.routers import SimpleRouter

from auth_apps.serializer import TeacherUserProfileViewSet
from auth_apps.views import CustomerTokenObtainPairView, CustomerTokenRefreshView,RegisterCreateAPIView

urlpatterns=[
    path('login/', CustomerTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', RegisterCreateAPIView.as_view(), name='register'),
    path('token/refresh/', CustomerTokenRefreshView.as_view(), name='token_refresh'),
]
zones = SimpleRouter()
zones.register(r'Teachers', TeacherUserProfileViewSet)
urlpatterns += zones.urls



