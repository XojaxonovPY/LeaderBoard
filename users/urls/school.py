from django.urls import path

from users.views import SchoolCreateAPIView, SchoolListAPIView, SchoolDestroyAPIView, SchoolUpdateAPIView

urlpatterns = [
    path("school/create/", SchoolCreateAPIView.as_view()),
    path("school/list/", SchoolListAPIView.as_view()),
    path("school/delete/<int:pk>/", SchoolDestroyAPIView.as_view()),
    path("school/update/<int:pk>/", SchoolUpdateAPIView.as_view()),
]
