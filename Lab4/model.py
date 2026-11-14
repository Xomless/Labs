from dataclasses import dataclass
from datetime import datetime


@dataclass
class Income:
    date: datetime
    source: str
    amount: int

    def __post_init__(self) -> None:
        if not isinstance(self.date, datetime):
            raise TypeError("Дата должна иметь тип datetime.")

        if not isinstance(self.source, str) or not self.source.strip():
            raise ValueError("Источник дохода не должен быть пустым.")

        if isinstance(self.amount, bool) or not isinstance(self.amount, int):
            raise TypeError("Сумма дохода должна быть целым числом.")
