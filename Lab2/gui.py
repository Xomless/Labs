import tkinter as tk
from tkinter import messagebox, ttk

from model import Income
from parser import parse_income


class IncomeApp:
    def __init__(self, incomes: list[Income]) -> None:
        self.incomes = incomes

        self.root = tk.Tk()
        self.root.title("Доходы")
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
        self.table.heading("source", text="Источник")
        self.table.heading("amount", text="Сумма")

        self.table.column("date", width=120)
        self.table.column("source", width=400)
        self.table.column("amount", width=150)

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
            text="Добавить",
            command=self.add_income
        )
        add_button.pack(side=tk.LEFT, padx=5)

        delete_button = tk.Button(
            buttons_frame,
            text="Удалить",
            command=self.delete_income
        )
        delete_button.pack(side=tk.LEFT, padx=5)

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
        add_window = tk.Toplevel(self.root)
        add_window.title("Добавить доход")
        add_window.geometry("400x250")
        add_window.resizable(False, False)

        tk.Label(
            add_window,
            text="Дата (гггг.мм.дд):"
        ).pack(pady=(15, 5))

        date_entry = tk.Entry(add_window, width=35)
        date_entry.pack()

        tk.Label(
            add_window,
            text="Источник:"
        ).pack(pady=(10, 5))

        source_entry = tk.Entry(add_window, width=35)
        source_entry.pack()

        tk.Label(
            add_window,
            text="Сумма:"
        ).pack(pady=(10, 5))

        amount_entry = tk.Entry(add_window, width=35)
        amount_entry.pack()

        def save_new_income() -> None:
            text = (
                f'{date_entry.get()} '
                f'"{source_entry.get()}" '
                f'{amount_entry.get()}'
            )

            try:
                income = parse_income(text)
            except (ValueError, AttributeError):
                messagebox.showerror(
                    "Ошибка",
                    "Проверьте правильность введённых данных."
                )
                return

            self.incomes.append(income)
            self.update_table()

            add_window.destroy()

        tk.Button(
            add_window,
            text="Добавить",
            command=save_new_income
        ).pack(pady=15)

    def delete_income(self) -> None:
        selected_items = self.table.selection()

        if not selected_items:
            messagebox.showwarning(
                "Удаление",
                "Сначала выберите доход в таблице."
            )
            return

        selected_item = selected_items[0]
        item_index = self.table.index(selected_item)

        del self.incomes[item_index]

        self.update_table()

    def run(self) -> None:
        self.root.mainloop()