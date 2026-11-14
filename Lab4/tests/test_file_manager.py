
from datetime import datetime

from model import Income
from file_manager import load_incomes, save_incomes


def test_load_incomes(tmp_path):
    filename = tmp_path / "data.txt"

    filename.write_text(
        '2026.11.10 "Зарплата" 50000\n'
        '2026.11.11 "Подработка" 15000\n',
        encoding="utf-8"
    )

    incomes = load_incomes(str(filename))

    assert len(incomes) == 2
    assert incomes[0].source == "Зарплата"
    assert incomes[1].amount == 15000


def test_load_incomes_skips_invalid_lines(tmp_path):
    filename = tmp_path / "data.txt"

    filename.write_text(
        '2026.11.10 "Зарплата" 50000\n'
        'неправильная строка\n'
        '\n'
        '2026.11.11 "Подработка" 15000\n',
        encoding="utf-8"
    )

    incomes = load_incomes(str(filename))

    assert len(incomes) == 2


def test_save_incomes(tmp_path):
    filename = tmp_path / "result.txt"

    incomes = [
        Income(datetime(2026, 11, 10), "Зарплата", 50000),
        Income(datetime(2026, 11, 11), "Подработка", 15000)
    ]

    save_incomes(str(filename), incomes)

    content = filename.read_text(encoding="utf-8")

    assert '2026.11.10 "Зарплата" 50000' in content
    assert '2026.11.11 "Подработка" 15000' in content
