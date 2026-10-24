# core/serializers.py
import re
from typing import Optional, Set

from django.db import IntegrityError
from rest_framework import serializers, status
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.validators import (
    UniqueForDateValidator,
    UniqueTogetherValidator,
    UniqueValidator,
)


class ConflictException(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_code = "conflict"


class CustomModelSerializer(serializers.ModelSerializer):
    """Barcha maydonlardan oldindan SELECT yuboruvchi Unique validatorlarni olib tashlaydi (1 ta SQL tejaydi).

    save(), create() va update() amallarida yuz beradigan DB IntegrityError ni
    ushlab, uni toza maydon darajasidagi ValidationError ga aylantiradi.
    """

    def get_validators(self):
        validators = super().get_validators()
        return [
            v
            for v in validators
            if not isinstance(v, (UniqueTogetherValidator, UniqueForDateValidator))
        ]

    def get_fields(self):
        fields = super().get_fields()
        for field in fields.values():
            if getattr(field, "validators", None):
                field.validators = [
                    v for v in field.validators if not isinstance(v, UniqueValidator)
                ]
        return fields

    def _extract_field_from_error(
            self, exc: Exception, model_fields: Set[str]
    ) -> Optional[str]:
        err_str = str(exc)

        # PostgreSQL: Key (username)=(...) already exists.
        pg_match = re.search(r"Key \((.*?)\)=", err_str)
        if pg_match:
            field_name = pg_match.group(1).split(",")[0].strip()
            if field_name in model_fields:
                return field_name

        # SQLite: UNIQUE constraint failed: table.field
        sqlite_match = re.search(r"UNIQUE constraint failed: [^.]+\.(.+)", err_str)
        if sqlite_match:
            field_name = sqlite_match.group(1).strip()
            if field_name in model_fields:
                return field_name

        # MySQL / Umumiy regex: Duplicate entry '...' for key 'table.field'
        err_lower = err_str.lower()
        for field in model_fields:
            if (
                    f"'{field}'" in err_lower
                    or f".{field}" in err_lower
                    or f"_{field}_" in err_lower
            ):
                return field

        return None

    def _handle_integrity_error(self, exc: IntegrityError):
        model = getattr(getattr(self, "Meta", None), "model", None)
        if model:
            concrete_fields = {f.name for f in model._meta.concrete_fields}
            conflict_field = self._extract_field_from_error(exc, concrete_fields)

            if conflict_field:
                raise ConflictException({
                    conflict_field: [
                        f"A record with this {conflict_field} already exists."
                    ]
                })

        raise ValidationError(
            {"non_field_errors": ["A database integrity conflict occurred."]}
        )

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError as exc:
            self._handle_integrity_error(exc)

    def update(self, instance, validated_data):
        try:
            return super().update(instance, validated_data)
        except IntegrityError as exc:
            self._handle_integrity_error(exc)

    def save(self, **kwargs):
        try:
            return super().save(**kwargs)
        except IntegrityError as exc:
            self._handle_integrity_error(exc)
