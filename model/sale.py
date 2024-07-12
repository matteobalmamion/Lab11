import datetime
from dataclasses import dataclass

@dataclass
class Sale:
    retailer_code: int
    product_number: int
    date: datetime.date