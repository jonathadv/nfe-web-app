from django.contrib.auth.models import Group, User
from django.http import HttpResponseRedirect
from django.urls import reverse
from nfe_scanner.models import Nfe
from rest_framework import permissions, viewsets
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend

from nfeweb.api.models import NfeDbModel, ProductCategory, ProductDbModel
from nfeweb.api.serializers import (
    GroupSerializer,
    NfeCreateByUrlSerializer,
    NfeSerializer,
    NfeSerializerWithEntries,
    UserSerializer,
    ProductCategorySerializer,
    ProductSerializer,
)
from nfeweb.api.services import NfeDbService, NfeScanService


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = ProductDbModel.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["category__title", "metric_unit", "barcode"]

    def get_queryset(self):
        if "no_category" in self.request.query_params:
            return self.queryset.filter(category=None)
        return super().get_queryset()


class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["title"]


class NfeViewSet(viewsets.ModelViewSet):
    queryset = NfeDbModel.objects.all()
    serializer_class = NfeSerializerWithEntries


class NfeScanViewSet(viewsets.ModelViewSet):
    queryset = NfeDbModel.objects.all()
    serializer_class = NfeCreateByUrlSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        nfe_url = serializer.validated_data.get("url")
        scanned_nfe: Nfe = NfeScanService.scan_nfe(nfe_url)

        nfe_serializer: NfeSerializer = NfeDbService().create(nfe_url, scanned_nfe)

        return HttpResponseRedirect(
            redirect_to=reverse("nfe-detail", args=[nfe_serializer.data.get("id")])
        )


class NfeCodeReader(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "nfe.html"

    def get(self, request):
        return Response({"profiles": ""})
