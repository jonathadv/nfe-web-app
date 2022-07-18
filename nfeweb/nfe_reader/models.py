from decimal import Decimal
from enum import Enum

from arrow import Arrow
from pydantic import AnyHttpUrl, BaseModel


class Config(BaseModel):
    nfe_endpoint: AnyHttpUrl
    nfe_codes: set[str]


class MetricUnit(Enum):
    KG = "KG"
    UNIT = "UN"

    def __str__(self):
        return self.value


class NfeItem(BaseModel):
    barcode: str
    description: str
    quantity: Decimal
    metric_unit: MetricUnit
    unitary_price: Decimal
    total_amount: Decimal

    class Config:
        frozen = True

    def __str__(self) -> str:
        return f"{self.description} ({self.quantity} {self.metric_unit.value} * {self.unitary_price} = R${self.total_amount})"


class Nfe(BaseModel):
    access_key: str
    title: str
    issued_date: Arrow
    items: list[NfeItem] = []
    total_amount: Decimal
    raw_html: str

    def __lt__(self, other: "Nfe"):
        return self.issued_date < other.issued_date

    def __gt__(self, other: "Nfe"):
        return self.issued_date > other.issued_date

    def __str__(self):
        content = [
            f"Access Key: {self.access_key}\n"
            f"Title: {self.title}\n"
            f"Date: {self.issued_date}\n",
            f"Total Amount: {self.total_amount}\n",
        ]
        for item in self.items:
            content.append(str(item))

        return "\n".join(content)

    class Config:
        arbitrary_types_allowed = True
