import csv
import logging
from datetime import datetime
from decimal import Decimal

from nfeweb.nfe_reader.models import Nfe
from nfeweb.nfe_reader.sqlite import add_nfe, add_nfe_item, connect, create_tables

LOGGER = logging.getLogger(__name__)


def console_report(nfes: list[Nfe]):
    LOGGER.info("%s", "=" * 25 + "RESULT" + "=" * 25)
    for nfe in nfes:
        LOGGER.info(nfe)
        LOGGER.info("-" * 50)


NFE_DATE = "NFe Date"
NFE_TITLE = "NFe Title"
NFE_TOTAL_AMOUNT = "NFe Total Amount"
ITEM_CODE = "Code"
ITEM_DESCRIPTION = "Description"
ITEM_QUANTITY = "Quantity"
ITEM_METRIC_UNIT = "Metric Unit"
ITEM_UNITARY_PRICE = "Unitary Price"
ITEM_TOTAL_AMOUNT = "Total Amount"


def l10n_decimal(value: Decimal) -> str:
    return str(value).replace(".", ",")


def csv_report(nfes: list[Nfe]):
    now = datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
    report_name = f"report-{now}.csv"
    fieldnames = [
        NFE_DATE,
        NFE_TITLE,
        NFE_TOTAL_AMOUNT,
        ITEM_CODE,
        ITEM_DESCRIPTION,
        ITEM_QUANTITY,
        ITEM_METRIC_UNIT,
        ITEM_UNITARY_PRICE,
        ITEM_TOTAL_AMOUNT,
    ]

    LOGGER.info("Writing CSV report '%s'.", report_name)
    with open(report_name, "w", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for nfe in nfes:
            nfe_columns = {
                NFE_DATE: nfe.issued_date,
                NFE_TITLE: nfe.title,
                NFE_TOTAL_AMOUNT: l10n_decimal(nfe.total_amount),
            }
            for item in nfe.items:
                item_columns = {
                    ITEM_CODE: item.barcode,
                    ITEM_DESCRIPTION: item.description,
                    ITEM_QUANTITY: l10n_decimal(item.quantity),
                    ITEM_METRIC_UNIT: item.metric_unit.value,
                    ITEM_UNITARY_PRICE: l10n_decimal(item.unitary_price),
                    ITEM_TOTAL_AMOUNT: l10n_decimal(item.total_amount),
                }
                writer.writerow({**nfe_columns, **item_columns})

    LOGGER.info("CSV report '%s' created.", report_name)


def sqlite_report(nfes: list[Nfe]):
    conn = connect()
    create_tables(conn)
    for nfe in nfes:
        add_nfe(conn, **nfe.dict())
        for item in nfe.items:
            add_nfe_item(conn, **item.dict(), nfe_access_key=nfe.access_key)
