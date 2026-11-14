
from datetime import datetime

from model import Income
from command_processor import execute_command


incomes = [
    Income(datetime(2026, 11, 10), "Зарплата", 50000),
    Income(datetime(2026, 11, 11), "Подработка", 15000),
]

print("Исходные доходы:", len(incomes))

print(execute_command(
    "ADD 2026.11.13;Стипендия;5000", incomes
))

print("После ADD:", len(incomes))

print(execute_command(
    "REM amount < 10000", incomes
))

print("После REM:", len(incomes))

print(execute_command(
    "SAVE result.txt", incomes
))
