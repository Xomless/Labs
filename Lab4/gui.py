
import tkinter as tk
from tkinter import messagebox, ttk, filedialog, simpledialog

from model import Income
from parser import parse_income
from command_processor import execute_command


class IncomeApp:
    def __init__(self, incomes: list[Income]) -> None:
        self.incomes = incomes

        self.root = tk.Tk()
        self.root.title("Учет доходов")
        self.root.geometry("750x450")

        self.create_table()
        self.create_buttons()
        self.update_table()

    def create_table(self) -> None:
        columns = ("date", "source", "amount")

        self.table = ttk.Treeview(
            self.root,
            columns=columns,
            show="headings"
        )

        self.table.heading("date", text="Дата")
        self.table.heading("source", text="Источник дохода")
        self.table.heading("amount", text="Сумма")

        self.table.column("date", width=150, anchor=tk.CENTER)
        self.table.column("source", width=400)
        self.table.column("amount", width=150, anchor=tk.CENTER)

        self.table.pack(
            fill=tk.BOTH,
            expand=True,
            padx=10,
            pady=10
        )

    def create_buttons(self) -> None:
        buttons_frame = tk.Frame(self.root)
        buttons_frame.pack(pady=10)

        add_button = tk.Button(
            buttons_frame,
            text="Добавить доход",
            command=self.add_income
        )
        add_button.pack(side=tk.LEFT, padx=5)

        delete_button = tk.Button(
            buttons_frame,
            text="Удалить доход",
            command=self.delete_income
        )
        delete_button.pack(side=tk.LEFT, padx=5)

        commands_button = tk.Button(
            buttons_frame,
            text="Выполнить команды",
            command=self.run_commands
        )
        commands_button.pack(side=tk.LEFT, padx=5)

    def update_table(self) -> None:
        for item in self.table.get_children():
            self.table.delete(item)

        for income in self.incomes:
            self.table.insert(
                "",
                tk.END,
                values=(
                    income.date.strftime("%Y.%m.%d"),
                    income.source,
                    income.amount
                )
            )

    def add_income(self) -> None:
        date = simpledialog.askstring(
            "Добавление дохода",
            "Введите дату (ГГГГ.ММ.ДД):",
            parent=self.root
        )
        if date is None:
            return

        source = simpledialog.askstring(
            "Добавление дохода",
            "Введите источник дохода:",
            parent=self.root
        )
        if source is None:
            return

        amount = simpledialog.askstring(
            "Добавление дохода",
            "Введите сумму дохода:",
            parent=self.root
        )
        if amount is None:
            return

        try:
            income = parse_income(
                f'{date.strip()} "{source.strip()}" {amount.strip()}'
            )
            self.incomes.append(income)
            self.update_table()
            messagebox.showinfo(
                "Успешно",
                "Доход добавлен."
            )
        except (ValueError, TypeError) as error:
            messagebox.showerror(
                "Ошибка",
                str(error)
            )

    def delete_income(self) -> None:
        selected = self.table.selection()

        if not selected:
            messagebox.showwarning(
                "Внимание",
                "Сначала выберите доход в таблице."
            )
            return

        index = self.table.index(selected[0])

        del self.incomes[index]
        self.update_table()

        messagebox.showinfo(
            "Успешно",
            "Доход удален."
        )

    def run_commands(self) -> None:
        filename = filedialog.askopenfilename(
            title="Выберите файл с командами",
            filetypes=[("Текстовые файлы", "*.txt")]
        )

        if not filename:
            return

        results = []

        try:
            with open(filename, "r", encoding="utf-8") as file:
                for line_number, line in enumerate(file, start=1):
                    if not line.strip():
                        continue

                    try:
                        result = execute_command(line, self.incomes)
                        results.append(
                            f"Строка {line_number}: {result}"
                        )
                    except (ValueError, TypeError, OSError) as error:
                        results.append(
                            f"Строка {line_number}: ошибка - {error}"
                        )

            self.update_table()

            messagebox.showinfo(
                "Результат выполнения команд",
                "\n".join(results) if results else "Файл команд пуст."
            )

        except OSError as error:
            messagebox.showerror(
                "Ошибка",
                f"Не удалось открыть файл: {error}"
            )

    def run(self) -> None:
        self.root.mainloop()
