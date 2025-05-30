from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from nfeweb.api.urls import api_router, code_reader, uncategorized_products

urlpatterns = [
    path("nfeweb/admin/", admin.site.urls),
    path("nfeweb/auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("nfeweb/", include(api_router.urls)),
    code_reader,
    uncategorized_products,
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
