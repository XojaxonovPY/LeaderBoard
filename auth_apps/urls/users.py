from django.urls import path

from auth_apps.views.users import StudentsListAPIView, UserProfileAPIView

urlpatterns = [
    path('users/students/', StudentsListAPIView.as_view(), name='students-list'),
    path('users/profile/', UserProfileAPIView.as_view(), name='user-profile'),

]





