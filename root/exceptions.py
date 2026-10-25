import logging

from django.core.exceptions import (
    PermissionDenied,
    ValidationError as DjangoValidationError,
)
from django.http import Http404
from rest_framework import exceptions, status
from rest_framework.response import Response
from rest_framework.views import exception_handler

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if isinstance(exc, Http404):
        exc = exceptions.NotFound(*(exc.args))
        response = exception_handler(exc, context)
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied(*(exc.args))
        response = exception_handler(exc, context)
    elif isinstance(exc, DjangoValidationError):
        exc = exceptions.ValidationError(detail=exc.message_dict or exc.messages)
        response = exception_handler(exc, context)

    if response is None:
        logger.error(
            f"Unexpected server error:{exc}",
            exc_info=True,
            extra={"view": context.get("view")},
        )
        return Response(
            {
                "success": False,
                "message": "An internal system error occurred. Please try again.",
                "errors": None,
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    error_data = response.data
    message = "An error occurred."
    errors = None

    if isinstance(error_data, dict):
        if "detail" in error_data and len(error_data) == 1:
            message = str(error_data["detail"])
        else:
            message = "An error was detected in the entered data."
            errors = error_data
    elif isinstance(error_data, list):
        message = " ".join([str(err) for err in error_data])
        errors = error_data
    elif isinstance(error_data, str):
        message = error_data
    logger.error(message, exc_info=True)
    response.data = {
        "success": False,
        "message": message,
        "errors": errors,
    }

    return response
