
from datetime import datetime

import pytest

from model import Income
from command_processor import execute_command


def create_incomes():
    return [
        Income(datetime(2026, 11, 10), "Зарплата", 50000),
        Income(datetime(2026, 11, 11), "Подработка", 15000),
        Income(datetime(2026, 11, 12), "Подарок", 3000),
    ]


def test_add_income():
    incomes = create_incomes()

    result = execute_command(
        "ADD 2026.11.13;Стипендия;5000",
        incomes
    )

    assert len(incomes) == 4
    assert incomes[-1].source == "Стипендия"
    assert incomes[-1].amount == 5000
    assert "добавлен" in result


def test_remove_by_amount():
    incomes = create_incomes()

    execute_command("REM amount < 10000", incomes)

    assert len(incomes) == 2
    assert all(income.amount >= 10000 for income in incomes)


def test_remove_by_source():
    incomes = create_incomes()

    execute_command("REM source = Зарплата", incomes)

    assert len(incomes) == 2
    assert all(income.source != "Зарплата" for income in incomes)


def test_remove_by_date():
    incomes = create_incomes()

    execute_command("REM date < 2026.11.11", incomes)

    assert len(incomes) == 2
    assert all(
        income.date >= datetime(2026, 11, 11)
        for income in incomes
    )


def test_save_incomes(tmp_path):
    incomes = create_incomes()
    filename = tmp_path / "result.txt"

    execute_command(f"SAVE {filename}", incomes)

    assert filename.exists()

    content = filename.read_text(encoding="utf-8")
    assert "Зарплата" in content
    assert "Подработка" in content
    assert "Подарок" in content


def test_unknown_command():
    incomes = create_incomes()

    with pytest.raises(ValueError):
        execute_command("UNKNOWN test", incomes)


def test_add_invalid_income():
    incomes = create_incomes()

    with pytest.raises(ValueError):
        execute_command("ADD неправильная_дата;Стипендия;5000", incomes)

    assert len(incomes) == 3


def test_empty_command():
    incomes = create_incomes()

    with pytest.raises(ValueError):
        execute_command("", incomes)

from parser import income_to_string


def test_model_invalid_date():
    with pytest.raises(TypeError):
        Income("2026.11.10", "Зарплата", 50000)


def test_model_empty_source():
    with pytest.raises(ValueError):
        Income(datetime(2026, 11, 10), "", 50000)


def test_model_invalid_amount():
    with pytest.raises(TypeError):
        Income(datetime(2026, 11, 10), "Зарплата", 5000.5)


def test_income_to_string():
    income = Income(
        datetime(2026, 11, 10),
        "Зарплата",
        50000
    )

    result = income_to_string(income)

    assert result == '2026.11.10 "Зарплата" 50000'


def test_add_invalid_date():
    incomes = create_incomes()

    with pytest.raises(ValueError):
        execute_command(
            "ADD 2026.13.40;Стипендия;5000",
            incomes
        )

    assert len(incomes) == 3
