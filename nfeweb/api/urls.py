from django.urls import path
from rest_framework import routers

from nfeweb.api import views

api_router = routers.DefaultRouter()
api_router.register(r"users", views.UserViewSet)
api_router.register(r"groups", views.GroupViewSet)
api_router.register(r"nfe-scan", views.NfeScanViewSet, basename="nfe-scan")
api_router.register(r"nfe", views.NfeViewSet, basename="nfe")
api_router.register(r"product-category", views.ProductCategoryViewSet, basename="product-category")
api_router.register(r"product", views.ProductViewSet, basename="product")

code_reader = path("nfeweb/nfe-scan-result", views.NfeScanResult.as_view(), name="nfe-scan-result")
uncategorized_products = path(
    "nfeweb/uncategorized-products",
    views.UncategorizedProducts.as_view(),
    name="uncategorized-products",
)
