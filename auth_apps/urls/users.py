from django.urls import path

from auth_apps.views.users import StudentsListAPIView, UserProfileRetrieveAPIView

urlpatterns = [
    path('users/students/', StudentsListAPIView.as_view(), name='students-list'),
    path('users/profile/', UserProfileRetrieveAPIView.as_view(), name='user-profile'),

]





