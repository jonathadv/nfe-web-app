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


class AddressDbModel(BaseModel):
    line1 = models.CharField(max_length=100, null=True)
    line2 = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=50, null=True)
    country = models.CharField(max_length=50, null=True)
    zip_code = models.CharField(max_length=20, null=True)

    class Meta:
        db_table = "address"


class ProductCategory(BaseModel):
    title = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = "product_category"

    def __str__(self):
        return f"{self.__class__.__name__}(title={self.title})"


class ProductDbModel(BaseModel):
    class MetricUnit(models.TextChoices):
        KG = "KG", _("KG")
        UNIT = "UNIT", _("UNIT")

    barcode = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    metric_unit = models.CharField(max_length=10, choices=MetricUnit.choices)
    category = models.ForeignKey(
        ProductCategory, on_delete=models.PROTECT, related_name="product", null=True
    )

    class Meta:
        db_table = "product"


class NfeIssuerDbModel(BaseModel):
    name = models.CharField(max_length=255)
    national_registration_code = models.CharField(max_length=255)
    state_registration_code = models.CharField(max_length=255)
    address = models.ForeignKey(AddressDbModel, on_delete=models.PROTECT, related_name="nfe_issue")

    class Meta:
        db_table = "nfe_issuer"


class NfeConsumerDbModel(BaseModel):
    identification = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = "nfe_consumer"


class NfeDbModel(BaseModel):
    class PaymentType(models.TextChoices):
        CREDIT_CARD = "CREDIT_CARD", _("Credit Card")
        DEBIT_CARD = "DEBIT_CARD", _("Debit Card")
        MONEY = "MONEY", _("Money")
        STORE_CARD = "STORE_CARD", _("Store Card")
        FOOD_VOUCHER = "FOOD_VOUCHER", _("Food Voucher")

    issuer = models.ForeignKey(NfeIssuerDbModel, on_delete=models.PROTECT, related_name="nfes")
    consumer = models.ForeignKey(
        NfeConsumerDbModel, on_delete=models.PROTECT, related_name="consumer"
    )
    issued_date = models.DateTimeField()
    access_key = models.CharField(max_length=255, unique=True)
    total_amount = models.FloatField()
    total_discounts = models.FloatField()
    raw_html = models.TextField()
    url = models.URLField(max_length=2048)
    payment_type = models.CharField(max_length=20, choices=PaymentType.choices)

    class Meta:
        db_table = "nfe"


class NfeEntryDbModel(BaseModel):
    nfe = models.ForeignKey(NfeDbModel, on_delete=models.PROTECT, related_name="entries")
    product = models.ForeignKey(
        ProductDbModel, on_delete=models.PROTECT, related_name="nfe_entries"
    )
    quantity = models.FloatField()
    unitary_price = models.FloatField()
    total_price = models.FloatField()

    class Meta:
        db_table = "nfe_entry"
