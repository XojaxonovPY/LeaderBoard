from django.urls import path
from auth_apps.views import CustomerTokenObtainPairView, CustomerTokenRefreshView

urlpatterns=[
    path('login/', CustomerTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomerTokenRefreshView.as_view(), name='token_refresh'),
]