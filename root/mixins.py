from typing import Any

from django.utils import timezone
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.request import Request
from rest_framework.response import Response


class CustomUpdateModelMixin:
    """
    1 ta yagona toza SQL so'rov bilan ishlovchi ultra-tezkor UPDATE mixini.
    - 2 ta so'rovdan (SELECT + UPDATE) qochadi, to'g'ridan-to'g'ri 1 ta SQL UPDATE bajaradi;
    - Model ichidagi auto_now=True (masalan, updated_at) maydonlarini o'sha 1 ta SQL so'rov
      ichida avtomatik tarzda timezone.now() bilan yangilaydi;
    - Serializerdagi mavjud bo'lmagan no-field maydonlarni tozalab, bazada crash bo'lishining oldini oladi;
    - Obyekt topilmasa yoki queryset filteriga tushmasa darhol NotFound (404) qaytaradi.
    """

    def update(self: Any, request: Request, *args: Any, **kwargs: Any):
        partial = kwargs.pop('partial', False)
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        lookup_value = kwargs[lookup_url_kwarg]
        serializer = self.get_serializer(data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        if partial and not validated_data:
            return Response({self.lookup_field: lookup_value}, status=status.HTTP_200_OK)

        model = self.get_queryset().model
        clean_update_data = {}

        for field in model._meta.concrete_fields:
            if field.name in validated_data:
                val = validated_data[field.name]
                clean_update_data[field.attname] = getattr(val, 'pk', val)
            elif field.attname in validated_data:
                clean_update_data[field.attname] = validated_data[field.attname]
            elif getattr(field, 'auto_now', False) and validated_data:
                clean_update_data[field.name] = timezone.now()

        filter_kwargs = {self.lookup_field: lookup_value}
        update_count = (
            self.filter_queryset(self.get_queryset())
            .filter(**filter_kwargs)
            .update(**clean_update_data)
        )

        if update_count == 0:
            raise NotFound(detail=f"Data is not found: {model.__name__}")

        response_data = {
            self.lookup_field: lookup_value,
            **validated_data
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def partial_update(self, request: Request, *args: Any, **kwargs: Any):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class CustomDestroyModelMixin:
    """
    1 ta yagona toza SQL so'rov bilan ishlovchi ultra-tezkor DELETE mixini.
    - Ortiqcha SELECT so'rovisiz to'g'ridan-to'g'ri 1 ta SQL DELETE bajaradi;
    - Agar obyekt topilmasa NotFound (404) qaytaradi.
    """

    def destroy(self: Any, request: Request, *args: Any, **kwargs: Any):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        lookup_value = kwargs[lookup_url_kwarg]
        filter_kwargs = {self.lookup_field: lookup_value}

        delete_count, _ = (
            self.filter_queryset(self.get_queryset()).filter(**filter_kwargs).delete()
        )
        if delete_count == 0:
            raise NotFound(detail=f"Data is not found: {self.get_queryset().model.__name__}")

        return Response(status=status.HTTP_204_NO_CONTENT)
