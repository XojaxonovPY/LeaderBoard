from django.urls import path

from users.views import CourseCreateAPIView, CourseListAPIView, CourseDestroyAPIView, CourseUpdateAPIView

urlpatterns = [
    path("course/create/", CourseCreateAPIView.as_view()),
    path("course/list/", CourseListAPIView.as_view()),
    path("course/delete/<int:pk>/", CourseDestroyAPIView.as_view()),
    path("course/update/<int:pk>/", CourseUpdateAPIView.as_view()),
]
