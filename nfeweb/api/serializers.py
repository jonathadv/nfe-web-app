import logging

from django.contrib.auth.models import Group, User
from rest_framework import serializers

from nfeweb.api.models import (
    AddressDbModel,
    NfeConsumerDbModel,
    NfeDbModel,
    NfeEntryDbModel,
    NfeIssuerDbModel,
    ProductCategory,
    ProductDbModel,
)

LOGGER = logging.getLogger(__name__)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "groups"]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = "__all__"


class NfeCreateByUrlSerializer(serializers.Serializer):
    url = serializers.URLField()

    def create(self, validated_data):
        super().create(validated_data)

    def update(self, instance, validated_data):
        super().update(validated_data)


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressDbModel
        fields = "__all__"


class IssuerSerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=False)

    def create(self, validated_data):
        address = self.get_address(validated_data.pop("address"))
        instance = NfeIssuerDbModel.objects.create(**validated_data, address=address)
        return instance

    @staticmethod
    def get_address(address: dict) -> dict | AddressDbModel:
        try:
            return AddressDbModel.objects.get(**address)
        except AddressDbModel.DoesNotExist:
            LOGGER.info("Address %s not found. Creating a new one. ", address)
            address = AddressDbModel.objects.create(**address)
            return address

    class Meta:
        model = NfeIssuerDbModel
        fields = "__all__"


class ConsumerSerializer(serializers.ModelSerializer):
    class Meta:
        model = NfeConsumerDbModel
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDbModel
        fields = "__all__"


class NfeEntrySerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        instance = NfeEntryDbModel.objects.create(**validated_data)
        return instance

    class Meta:
        model = NfeEntryDbModel
        fields = "__all__"


class NfeSerializer(serializers.ModelSerializer):
    issuer = IssuerSerializer(read_only=False)

    def create(self, validated_data):
        issuer = IssuerSerializer(data=validated_data.pop("issuer"))
        issuer.is_valid(raise_exception=True)
        issuer.save()

        issuer = NfeIssuerDbModel.objects.get(id=issuer.data.get("id"))

        instance = NfeDbModel.objects.create(**validated_data, issuer=issuer)
        return instance

    class Meta:
        model = NfeDbModel
        fields = "__all__"


class NfeSerializerWithEntries(NfeSerializer):
    entries = NfeEntrySerializer(many=True)
