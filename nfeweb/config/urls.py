from django.contrib import admin
from django.urls import include, path

from nfeweb.api.urls import api_router, code_reader

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("", include(api_router.urls)),
    code_reader,
]
