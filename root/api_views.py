from urllib.request import Request

from rest_framework.generics import GenericAPIView

from root.mixins import CustomUpdateModelMixin, CustomDestroyModelMixin


class CustomUpdateAPIView(CustomUpdateModelMixin, GenericAPIView):
    def put(self, request: Request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request: Request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class CustomDestroyAPIView(CustomDestroyModelMixin, GenericAPIView):
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)