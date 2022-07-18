from django.contrib.auth.models import Group, User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions, status, viewsets
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from nfeweb.api.models import Mall, Nfe, NfeEntry, Product
from nfeweb.api.serializers import (
    GroupSerializer,
    NfeCreationSerializer,
    NfeSerializer,
    UserSerializer,
)
from nfeweb.nfe_reader.nfe import parse_nfe_by_url


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


class NfeViewSet(viewsets.ModelViewSet):
    queryset = Nfe.objects.all()
    serializer_class = NfeCreationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        nfe_url = serializer.data.get("url")
        nfe_model = parse_nfe_by_url(nfe_url)

        try:
            db_mall = Mall.objects.get(name=nfe_model.title)
        except ObjectDoesNotExist as err:
            db_mall = Mall.objects.create(name=nfe_model.title, address="", identity_code="")

        db_nfe = Nfe.objects.create(
            url=nfe_url,
            mall=db_mall,
            access_key=nfe_model.access_key,
            title=nfe_model.title,
            issued_date=nfe_model.issued_date.datetime,
            total_amount=nfe_model.total_amount,
            raw_html=nfe_model.raw_html,
        )

        for product_model in nfe_model.items:
            try:
                db_product = Product.objects.get(barcode=product_model.barcode)
            except ObjectDoesNotExist as err:
                db_product = Product.objects.create(
                    barcode=product_model.barcode,
                    description=product_model.description,
                )

            db_entry = NfeEntry.objects.create(
                nfe=db_nfe,
                product=db_product,
                quantity=product_model.quantity,
                unitary_price=product_model.unitary_price,
                total_amount=product_model.total_amount,
            )

        nfe_serializer = NfeSerializer(db_nfe)

        headers = self.get_success_headers(serializer.data)
        return Response(nfe_serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class NfeCodeReader(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "nfe.html"

    def get(self, request):
        request.data
        return Response({"profiles": ""})
