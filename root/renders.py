# core/renderers.py
from decimal import Decimal
from typing import Any
from uuid import UUID

import orjson
from django.core.files.base import File
from django.core.files.uploadedfile import UploadedFile
from django.db.models.fields.files import FieldFile
from django.utils.functional import Promise
from rest_framework.renderers import BaseRenderer


def _orjson_default(obj: Any) -> Any:
    """orjson standart tushunmaydigan Django turlarini xavfsiz o'giruvchi fallback funksiya."""
    # 1. Django lazy stringlar (masalan: gettext_lazy, validation messagelar)
    if isinstance(obj, Promise):
        return str(obj)

    # 2. Decimal maydonlar (narxlar, summalar) - aniqlik yo'qolmasligi uchun str qilinadi
    if isinstance(obj, Decimal):
        return str(obj)

    # 3. Agar numpy yoki shunga o'xshash massivlar bo'lsa
    if hasattr(obj, "tolist"):
        return obj.tolist()
    if isinstance(obj, UploadedFile):
        return obj.name

        # 2. Bazadan o'qilgan model rasmlari/fayllari (FieldFile, ImageFieldFile)
    if isinstance(obj, FieldFile):
        if not obj:  # agar rasm bo'sh bo'lsa (null/blank)
            return None
        try:
            return obj.url  # /media/avatars/user.jpg kabi to'liq yoki nisbiy URL
        except ValueError:
            return obj.name

        # 3. Oddiy Django/Python File obyektlari
    if isinstance(obj, File):
        return obj.name

    if isinstance(obj, UUID):
        return str(obj)

    raise TypeError(f"Type {type(obj)} is not JSON serializable")


class ORJSONRenderer(BaseRenderer):
    media_type = "application/json"
    format = "json"
    charset = None

    def render(self, data: Any, accepted_media_type=None, renderer_context=None) -> bytes:
        if data is None:
            return b""
        options = orjson.OPT_NON_STR_KEYS

        return orjson.dumps(data, default=_orjson_default, option=options)
