import logging

from nfe_scanner.models import Nfe, NfeConsumer, NfeItem
from nfe_scanner.nfe import scan_nfe
from rest_framework.exceptions import ValidationError

from nfeweb.api.models import NfeConsumerDbModel, ProductDbModel
from nfeweb.api.serializers import (
    ConsumerSerializer,
    NfeEntrySerializer,
    NfeSerializer,
    ProductSerializer,
)

LOGGER = logging.getLogger(__name__)


class NfeScanService:
    @staticmethod
    def scan_nfe(url: str) -> Nfe:
        return scan_nfe(url)


class NfeDbService:
    def create(self, url: str, scanned_nfe: Nfe) -> NfeSerializer:
        LOGGER.info("Saving new NFe model with access key '%s'", scanned_nfe.access_key)

        nfe_serializer = NfeSerializer(
            data={
                "issuer": scanned_nfe.issuer.dict(),
                "consumer": self.maybe_create_consumer(scanned_nfe.consumer),
                "issued_date": scanned_nfe.issued_date,
                "access_key": scanned_nfe.access_key,
                "total_amount": scanned_nfe.total_amount,
                "total_discounts": scanned_nfe.total_discounts,
                "payment_type": scanned_nfe.payment_type.value,
                "raw_html": scanned_nfe.raw_html,
                "url": url,
            }
        )
        nfe_serializer.is_valid(raise_exception=True)
        nfe_serializer.save()

        for nfe_item in scanned_nfe.items:
            self.create_nfe_entry(nfe_item, nfe_serializer.data.get("id"))

        return nfe_serializer

    def create_nfe_entry(self, item: NfeItem, nfe_id: str):
        product_id = self.maybe_create_product(item)
        LOGGER.info(
            "Saving new NFe entry for product id '%s'; barcode '%s'; description %s",
            product_id,
            item.barcode,
            item.description,
        )

        entry_serializer = NfeEntrySerializer(
            data={
                "nfe": nfe_id,
                "product": product_id,
                "quantity": item.quantity,
                "unitary_price": item.unitary_price,
                "total_price": item.total_price,
            }
        )

        entry_serializer.is_valid(raise_exception=True)
        entry_serializer.save()

    @staticmethod
    def maybe_create_consumer(consumer: NfeConsumer):
        try:
            consumer_serializer = ConsumerSerializer(data=consumer.dict())
            consumer_serializer.is_valid(raise_exception=True)
            consumer_serializer.save()
            consumer_id = consumer_serializer.data.get("id")
        except ValidationError as err:
            if "already exists" in str(err.args[0]):
                consumer_id = NfeConsumerDbModel.objects.get(
                    identification=consumer.identification
                ).id
            else:
                raise
        return consumer_id

    @staticmethod
    def maybe_create_product(item: NfeItem) -> str:
        try:
            product_serializer = ProductSerializer(
                data={
                    "barcode": item.barcode,
                    "description": item.description,
                    "metric_unit": item.metric_unit.value,
                }
            )
            product_serializer.is_valid(raise_exception=True)
            LOGGER.info(
                "Creating new product with barcode '%s' and description '%s' ",
                item.barcode,
                item.description,
            )

            product_serializer.save()
            product_id = product_serializer.data.get("id")
        except ValidationError as err:
            if "already exists" in str(err.args[0]):
                LOGGER.info(
                    "Product with barcode '%s' and description '%s' already exists! Using it.",
                    item.barcode,
                    item.description,
                )
                product = ProductDbModel.objects.get(barcode=item.barcode)
                product_id = product.id

                if product.description != item.description:
                    raise ValidationError(
                        f"Found product with barcode {item.barcode} but description does not match: "
                        f"Description in db: {product.description}; "
                        f"Description in new entry: {item.description};"
                    ) from err

            else:
                raise
        return product_id
