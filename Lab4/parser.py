import re
from datetime import datetime

from model import Income


_PATTERN = re.compile(r'^(\d{4}\.\d{2}\.\d{2})\s+"([^"]+)"\s+(\d+)$')


def parse_income(text: str) -> Income:
    """Преобразует строку с доходом в объект Income."""
    match = _PATTERN.fullmatch(text.strip())

    if match is None:
        raise ValueError(
            'Неверный формат. Ожидается: 2026.11.13 "Зарплата" 50000'
        )

    try:
        date = datetime.strptime(match.group(1), "%Y.%m.%d")
    except ValueError as error:
        raise ValueError("Указана неправильная дата.") from error

    source = match.group(2).strip()
    amount = int(match.group(3))

    return Income(date=date, source=source, amount=amount)


def income_to_string(income: Income) -> str:
    return (
        f'{income.date.strftime("%Y.%m.%d")} '
        f'"{income.source}" '
        f'{income.amount}'
    )
