from file_manager import load_incomes
from gui import IncomeApp
from logger_config import configure_logger


def main() -> None:
    configure_logger()
    incomes = load_incomes("data.txt")
    app = IncomeApp(incomes)
    app.run()


if __name__ == "__main__":
    main()


