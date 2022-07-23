from django.core.management.base import BaseCommand
from django.db import connection

VIEW_NAME = "all_nfe_items"
CREATE_VIEW_STATEMENT = f"""
CREATE OR REPLACE VIEW {VIEW_NAME} AS
SELECT n.id AS nfe_id,
       n.issued_date,
       n.access_key,
       n.total_amount,
       n.total_discounts,
       ni."name" AS issuer_name,
       nc.identification AS consumer_identification,
       concat(a.line1, ', ', a.line2, ' ', a.city, ', ', a.state, ', ', a.country) AS issuer_address,
       p.barcode AS item_barcode,
       p.description AS item_description,
       ne.unitary_price AS item_unitary_price,
       ne.total_price AS item_total_price
FROM nfe n
INNER JOIN nfe_consumer nc ON n.consumer_id = nc.id
INNER JOIN nfe_issuer ni ON n.issuer_id = ni.id
INNER JOIN address a ON ni.address_id = a.id
INNER JOIN nfe_entry ne ON ne.nfe_id = n.id
INNER JOIN product p ON p.id = ne.product_id;
"""


class Command(BaseCommand):
    help = "Create db schema"

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute(CREATE_VIEW_STATEMENT)
            self.stdout.write(self.style.SUCCESS(f"View '{VIEW_NAME}' successfully created"))
