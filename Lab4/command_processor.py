
import re
import operator
from datetime import datetime

from model import Income
from parser import parse_income
from file_manager import save_incomes


def execute_command(command: str, incomes: list[Income]) -> str:
    command = command.strip()

    if not command:
        raise ValueError("Пустая команда.")

    parts = command.split(maxsplit=1)
    action = parts[0].upper()

    if len(parts) < 2:
        raise ValueError("Не указан аргумент команды.")

    argument = parts[1].strip()

    if action == "ADD":
        fields = argument.split(";")

        if len(fields) != 3:
            raise ValueError(
                "Для ADD нужны дата, источник и сумма."
            )

        date, source, amount = [
            field.strip() for field in fields
        ]

        income = parse_income(
            f'{date} "{source}" {amount}'
        )

        incomes.append(income)

        return "Доход успешно добавлен."

    elif action == "REM":
        match = re.fullmatch(
            r"(amount|source|date)\s*(<=|>=|=|<|>)\s*(.+)",
            argument,
            re.IGNORECASE
        )

        if match is None:
            raise ValueError("Неверное условие REM.")

        field, sign, value = match.groups()
        field = field.lower()
        value = value.strip()

        if field == "amount":
            value = int(value)

        elif field == "date":
            value = datetime.strptime(
                value, "%Y.%m.%d"
            )

        elif field == "source":
            if sign != "=":
                raise ValueError(
                    "Для источника поддерживается только =."
                )
            value = value.strip('"')

        operations = {
            "<": operator.lt,
            ">": operator.gt,
            "=": operator.eq,
            "<=": operator.le,
            ">=": operator.ge
        }

        compare = operations[sign]

        old_count = len(incomes)

        if field == "amount":
            incomes[:] = [
                income for income in incomes
                if not compare(income.amount, value)
            ]

        elif field == "date":
            incomes[:] = [
                income for income in incomes
                if not compare(income.date, value)
            ]

        else:
            incomes[:] = [
                income for income in incomes
                if not compare(income.source, value)
            ]

        removed = old_count - len(incomes)

        return f"Удалено доходов: {removed}."

    elif action == "SAVE":
        save_incomes(argument, incomes)

        return f"Данные сохранены в файл: {argument}"

    else:
        raise ValueError(
            f"Неизвестная команда: {action}"
        )
