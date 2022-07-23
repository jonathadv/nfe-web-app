from django.contrib.auth.models import Group, User
from django.http import HttpResponseRedirect
from rest_framework import permissions, status, viewsets
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from nfe_reader.models import Nfe
from nfeweb.api.models import NfeDbModel
from nfeweb.api.serializers import (
    GroupSerializer,
    NfeCreateByUrlSerializer,
    NfeSerializer,
    NfeSerializerWithEntries,
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

        # return Response(result, status=status.HTTP_302_FOUND)

        return HttpResponseRedirect(redirect_to=f'/nfe/{nfe_serializer.data.get("id")}/')


class NfeCodeReader(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "nfe.html"

    def get(self, request):
        return Response({"profiles": ""})
