from dataclasses import dataclass
from datetime import datetime


@dataclass
class Income:
    date: datetime
    source: str
    amount: int