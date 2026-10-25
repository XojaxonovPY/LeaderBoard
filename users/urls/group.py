from django.urls import path

from users.views.group import GroupUpdateAPIView, GroupCreateAPIView, GroupListAPIView, GroupDestroyAPIView

urlpatterns = [
    path("group/create/", GroupCreateAPIView.as_view()),
    path("group/list/", GroupListAPIView.as_view()),
    path("group/delete/<int:pk>/", GroupDestroyAPIView.as_view()),
    path("group/update/<int:pk>/", GroupUpdateAPIView.as_view()),
]
