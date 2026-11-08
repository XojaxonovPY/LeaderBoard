from django.urls import path

from apps.views import BookCreateAPIView, BookListAPIView, BookDetailAPIView, BookUpdateAPIView

urlpatterns = [
    path('book/create/', BookCreateAPIView.as_view()),
    path('book/list/', BookListAPIView.as_view()),
    path('book/detail/<int:pk>', BookDetailAPIView.as_view()),
    path('book/update/<int:pk>', BookUpdateAPIView.as_view()),
]
