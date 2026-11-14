
import re
from datetime import datetime


class Income:
    def __init__(self, date: datetime, source: str, amount: int):
        self.date = date
        self.source = source
        self.amount = amount

    def __str__(self):
        return (
            f"Дата: {self.date.strftime('%Y.%m.%d')}\n"
            f"Источник: {self.source}\n"
            f"Сумма: {self.amount}"
        )


def parse_income(text: str) -> Income:
    pattern = r'^Income\s+(\d{4}\.\d{2}\.\d{2})\s+"([^"]+)"\s+(\d+)$'

    match = re.fullmatch(pattern, text.strip())

    if match is None:
        raise ValueError("Неверный формат данных!")

    date = datetime.strptime(match.group(1), "%Y.%m.%d")
    source = match.group(2)
    amount = int(match.group(3))

    return Income(date, source, amount)


def main():
    text = input("Введите описание дохода:\n")

    try:
        income = parse_income(text)
        print("\nСозданный объект:")
        print(income)

    except ValueError as error:
        print(f"\nОшибка: {error}")
        print('Пример правильного ввода:')
        print('Income 2026.11.13 "Зарплата" 50000')


if __name__ == "__main__":
    main()
