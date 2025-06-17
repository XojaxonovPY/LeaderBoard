from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.views import  TeacherModelViewSet

router=DefaultRouter()

router.register(r'homework', TeacherModelViewSet, basename='homework')  # TO‘G‘RISI

urlpatterns = [
    path('teachers/',include(router.urls))
]
