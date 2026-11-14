from parser import parse_income, income_to_string
from model import Income


def load_incomes(filename: str) -> list[Income]:
    incomes = []

    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if line:
                incomes.append(parse_income(line))

    return incomes


def save_incomes(filename: str, incomes: list[Income]) -> None:
    with open(filename, "w", encoding="utf-8") as file:
        for income in incomes:
            file.write(income_to_string(income) + "\n")