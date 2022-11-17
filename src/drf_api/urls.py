from django.urls import include, path
from rest_framework import routers
from src.drf_api import viewsets


router = routers.DefaultRouter()
router.register(r'check', viewsets.CheckViewSet)
router.register(r'printer/(?P<api_key>[0-9A-Za-z_\-]+)', viewsets.PrinterViewSet)
router.register(r'download-pdf',
                viewsets.ResponsePdfViewSet)


urlpatterns = [
    path('', include(router.urls)),
]