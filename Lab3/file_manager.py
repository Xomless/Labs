import logging

from model import Income
from parser import income_to_string, parse_income


logger = logging.getLogger(__name__)


def load_incomes(filename: str) -> list[Income]:
    incomes = []

    with open(filename, "r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()

            if not line:
                continue

            try:
                incomes.append(parse_income(line))
            except (ValueError, TypeError) as error:
                logger.warning(
                    "Строка %s пропущена: %s. Содержимое: %r",
                    line_number,
                    error,
                    line
                )

    return incomes


def save_incomes(filename: str, incomes: list[Income]) -> None:
    with open(filename, "w", encoding="utf-8") as file:
        for income in incomes:
            file.write(income_to_string(income) + "\n")
