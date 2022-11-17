"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path

from drf_yasg2.views import get_schema_view
from drf_yasg2 import openapi

api_info = openapi.Info(
    title="Snippets API",
    default_version='1.0.0',
    description='API documentation of App',
)

schema_view = get_schema_view(
    openapi.Info(
        title="Printer API",
        default_version='1.0.0',
        description='API documentation of App',
    ),
    public=True
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include([
        path('', include(('drf_api.urls', 'printer'), namespace='printers')),
        re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        path('swagger/schema/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-shema')
    ])),
]
