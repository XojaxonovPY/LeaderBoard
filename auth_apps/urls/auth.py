from django.urls import path

from auth_apps.views.auth import CustomerTokenObtainPairView, CustomerTokenRefreshView,RegisterCreateAPIView

urlpatterns=[
    path('login', CustomerTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', RegisterCreateAPIView.as_view(), name='register'),
    path('token/refresh/', CustomerTokenRefreshView.as_view(), name='token_refresh'),
]