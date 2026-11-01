from django.urls import path

from users.views import LeaderboardAPIView
from users.views import UserCreateAPIView, UserListAPIView, UserRetrieveAPIView, UserUpdateAPIView, UserDestroyAPIView

urlpatterns = [
    path("user/create.", UserCreateAPIView.as_view()),
    path("user/list/", UserListAPIView.as_view()),
    path("user/detail/<int:pk>", UserRetrieveAPIView.as_view()),
    path("user/update/<int:pk>", UserUpdateAPIView.as_view()),
    path("user/delete/<int:pk>", UserDestroyAPIView.as_view()),
    path('admin/groups/leaderboard/<int:pk>/', LeaderboardAPIView.as_view()),
]
