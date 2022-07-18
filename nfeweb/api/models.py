import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    class Meta:
        abstract = True


class Product(BaseModel):
    barcode = models.CharField(max_length=255, unique=True)
    description = models.TextField()

    class MetricUnit(models.TextChoices):
        KG = "KG", _("KG")
        UNIT = "UNIT", _("UNIT")


class Mall(BaseModel):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    identity_code = models.CharField(max_length=255)


class Nfe(BaseModel):
    mall = models.ForeignKey(Mall, on_delete=models.PROTECT, related_name="nfes")
    access_key = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=255)
    issued_date = models.DateTimeField()
    total_amount = models.FloatField()
    url = models.URLField()
    raw_html = models.TextField()


class NfeEntry(BaseModel):
    nfe = models.ForeignKey(Nfe, on_delete=models.PROTECT, related_name="entries")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="nfe_entries")
    quantity = models.FloatField()
    unitary_price = models.FloatField()
    total_amount = models.FloatField()
