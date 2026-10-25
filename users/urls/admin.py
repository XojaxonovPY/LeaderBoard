from django.urls import path
from rest_framework.routers import DefaultRouter

from users.views import GroupModelViewSet, UserCreateAPIView, UserListAPIView, UserRetrieveAPIView, UserUpdateAPIView, \
    UserDestroyAPIView
from users.views import LeaderboardAPIView

router = DefaultRouter()

router.register(r'groups', GroupModelViewSet, basename='group')

urlpatterns = [
    path("user/create.", UserCreateAPIView.as_view()),
    path("user/list/", UserListAPIView.as_view()),
    path("user/detail/<int:pk>", UserRetrieveAPIView.as_view()),
    path("user/update/<int:pk>", UserUpdateAPIView.as_view()),
    path("user/delete/<int:pk>", UserDestroyAPIView.as_view()),
    path('admin/groups/leaderboard/<int:pk>/', LeaderboardAPIView.as_view()),
]
