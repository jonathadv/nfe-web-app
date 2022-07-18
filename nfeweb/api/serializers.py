from django.contrib.auth.models import Group, User
from rest_framework import serializers

from nfeweb.api.models import Nfe


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "groups"]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]


class NfeCreationSerializer(serializers.Serializer):
    url = serializers.URLField()


class NfeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nfe
        fields = "__all__"
