# core/parsers.py
import orjson
from rest_framework.exceptions import ParseError
from rest_framework.parsers import BaseParser


class ORJSONParser(BaseParser):
    media_type = "application/json"

    def parse(self, stream, media_type=None, parser_context=None):
        try:
            return orjson.loads(stream.read())
        except orjson.JSONDecodeError as exc:
            raise ParseError(f"JSON decode exception: {exc}")
