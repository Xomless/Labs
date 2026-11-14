from file_manager import load_incomes
from gui import IncomeApp


def main() -> None:
    incomes = load_incomes("data.txt")

    app = IncomeApp(incomes)

    app.run()


if __name__ == "__main__":
    main()