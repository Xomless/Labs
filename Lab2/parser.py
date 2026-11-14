import re
from datetime import datetime

from model import Income


def parse_income(text: str) -> Income:
    pattern = r'^(\d{4}\.\d{2}\.\d{2})\s+"([^"]+)"\s+(\d+)$'

    match = re.match(pattern, text.strip())

    date = datetime.strptime(match.group(1), "%Y.%m.%d")
    source = match.group(2)
    amount = int(match.group(3))

    return Income(
        date=date,
        source=source,
        amount=amount
    )


def income_to_string(income: Income) -> str:
    return (
        f'{income.date.strftime("%Y.%m.%d")} '
        f'"{income.source}" '
        f'{income.amount}'
    )