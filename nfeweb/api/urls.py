from django.urls import path
from rest_framework import routers

from nfeweb.api import views

api_router = routers.DefaultRouter()
api_router.register(r"users", views.UserViewSet)
api_router.register(r"groups", views.GroupViewSet)
api_router.register(r"nfe", views.NfeViewSet)
code_reader = path("nfe-reader", views.NfeCodeReader.as_view(), name="code_reader")
