from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView

from apps.models import Book
from apps.serializer import BookModelSerializer, BookUpdateSerializer
from root.api_views import CustomUpdateAPIView
from users.permissions import IsSuperAdmin


@extend_schema(tags=['books'])
class BookCreateAPIView(CreateAPIView):
    serializer_class = BookModelSerializer
    permission_classes = [IsSuperAdmin]


@extend_schema(tags=['books'])
class BookListAPIView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookModelSerializer
    permission_classes = [IsSuperAdmin]


@extend_schema(tags=['books'])
class BookDetailAPIView(RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookModelSerializer
    lookup_field = 'pk'
    permission_classes = [IsSuperAdmin]


@extend_schema(tags=['books'])
class BookUpdateAPIView(CustomUpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookUpdateSerializer
    permission_classes = [IsSuperAdmin]
