from typing import Any

from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.request import Request
from rest_framework.response import Response


class CustomUpdateModelMixin:
    """
    Update a model instance.
    """

    def update(self: Any, request: Request, *args: Any, **kwargs: Any):
        partial = kwargs.pop('partial', False)
        lookup_url_kwark = self.lookup_url_kwarg or self.lookup_field
        lookup_value = kwargs[lookup_url_kwark]
        serializer = self.get_serializer(data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        filter_kwargs = {self.lookup_field: lookup_value}
        update_count = (
            self.filter_queryset(self.get_queryset()).filter(**filter_kwargs).update(**serializer.validated_data)
        )
        if update_count == 0:
            raise NotFound(detail="Data is not found:{}".format(self.get_queryset().model.__name__))
        response_data = {
            self.lookup_field: lookup_value,
            **serializer.validated_data
        }
        return Response(status=status.HTTP_200_OK, data=response_data)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class CustomDestroyModelMixin:
    """
    Destroy a model instance.
    """

    def destroy(self: Any, request: Request, *args: Any, **kwargs: Any):
        lookup_url_kwark = self.lookup_url_kwarg or self.lookup_field
        lookup_value = kwargs[lookup_url_kwark]
        filter_kwargs = {self.lookup_field: lookup_value}
        delete_count = (
            self.filter_queryset(self.get_queryset()).filter(**filter_kwargs).delete()
        )
        if delete_count == 0:
            raise NotFound(detail="Data is not found:{}".format(self.get_queryset().model.__name__))
        return Response(status=status.HTTP_204_NO_CONTENT)  
