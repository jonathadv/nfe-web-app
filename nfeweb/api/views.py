from django.contrib.auth.models import Group, User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django_filters.rest_framework import DjangoFilterBackend
from nfe_scanner.models import Nfe
from rest_framework import mixins, permissions, viewsets
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from nfeweb.api.models import NfeDbModel, ProductCategory, ProductDbModel, ProductType
from nfeweb.api.serializers import (
    GroupSerializer,
    NfeCreateByUrlSerializer,
    NfeSerializer,
    NfeSerializerWithEntries,
    ProductCategorySerializer,
    ProductSerializer,
    ProductTypeSerializers,
    UserSerializer,
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
    filterset_fields = ["product_type__category__title", "metric_unit", "barcode"]

    def get_queryset(self):
        if "no_category" in self.request.query_params:
            return self.queryset.filter(category=None)

        if "no_product_type" in self.request.query_params:
            return self.queryset.filter(product_type=None)

        return super().get_queryset()


class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["title"]


class ProductTypeViewSet(viewsets.ModelViewSet):
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializers
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["name"]


class NfeViewSet(viewsets.ModelViewSet):
    queryset = (
        NfeDbModel.objects.select_related("issuer")
        .select_related("issuer__address")
        .prefetch_related("entries")
    )
    serializer_class = NfeSerializerWithEntries
    ordering_fields = ["-created_at"]


class NfeScanViewSet(viewsets.ModelViewSet):
    queryset = NfeDbModel.objects.all()
    serializer_class = NfeCreateByUrlSerializer
    ordering_fields = ["-created_at"]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        nfe_url = serializer.validated_data.get("url")
        scanned_nfe: Nfe = NfeScanService.scan_nfe(nfe_url)

        nfe_serializer: NfeSerializer = NfeDbService().create(nfe_url, scanned_nfe)

        return HttpResponseRedirect(
            redirect_to=f"{reverse('nfe-scan-result')}?id={nfe_serializer.data.get('id')}"
        )


class NfeScanResult(APIView, mixins.UpdateModelMixin):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "nfe.html"

    def get(self, request):
        queryset = NfeDbModel.objects.get(id=request.GET.get("id"))
        uncategorized_products_quantity = len(
            ProductDbModel.objects.filter(product_type__category__isnull=True)
        )
        return Response(
            {
                "queryset": queryset,
                "uncategorized_products_quantity": uncategorized_products_quantity,
            }
        )


class UncategorizedProducts(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "uncategorized_products.html"

    def get(self, request):
        queryset = ProductDbModel.objects.filter(product_type__isnull=True)
        products = [ProductSerializer(value) for value in queryset]
        return Response(
            {
                "name": "Uncategorized Products",
                "products": products,
                "uncategorized_products": queryset,
                "product_type_serializer": ProductTypeSerializers,
                "product_category_serializer": ProductCategorySerializer,
            }
        )

    def post(self, request):
        product = get_object_or_404(ProductDbModel, pk=request.data.get("id"))
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()

        return redirect("uncategorized-products")
