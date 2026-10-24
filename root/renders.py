# core/renderers.py
from decimal import Decimal
from typing import Any

import orjson
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
