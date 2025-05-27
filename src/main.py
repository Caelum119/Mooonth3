import flet
from flet import (
    Page, TextField, ElevatedButton, Column,
    Text, AlertDialog, Row, ListView, IconButton,
    icons
)

def main(page: Page):
    page.title = "Учёт расходов"

    expenses = []  # список из словарей {"name": ..., "amount": ...}
    total_sum = 0

    # Виджеты
    name_input = TextField(label="Название расхода", width=300)
    amount_input = TextField(label="Сумма расхода", width=300, keyboard_type="number")
    expenses_list = Column()
    total_text = Text("Общая сумма расходов: 0", size=16, weight="bold")

    # Диалог редактирования
    edit_name = TextField(label="Название")
    edit_amount = TextField(label="Сумма", keyboard_type="number")
    edit_dialog = AlertDialog(modal=True)

    def update_total():
        nonlocal total_sum
        total_sum = sum(item["amount"] for item in expenses)
        total_text.value = f"Общая сумма расходов: {total_sum}"
        page.update()

    def refresh_list():
        expenses_list.controls.clear()
        for i, item in enumerate(expenses):
            expenses_list.controls.append(
                Row([
                    Text(f"{item['name']}: {item['amount']}"),
                    IconButton(icons.EDIT, tooltip="Редактировать", data=i, on_click=open_edit_dialog)
                ])
            )
        update_total()

    def add_expense(e):
        name = name_input.value.strip()
        amount_str = amount_input.value.strip()
        if not name or not amount_str:
            page.snack_bar = Text("Заполните все поля")
            page.snack_bar.open = True
            page.update()
            return

        try:
            amount = float(amount_str)
            if amount <= 0:
                raise ValueError()
        except ValueError:
            page.snack_bar = Text("Сумма должна быть положительным числом")
            page.snack_bar.open = True
            page.update()
            return

        expenses.append({"name": name, "amount": amount})
        name_input.value = ""
        amount_input.value = ""
        refresh_list()

    def open_edit_dialog(e):
        index = e.control.data
        item = expenses[index]
        edit_name.value = item["name"]
        edit_amount.value = str(item["amount"])

        def save_edit(ev):
            new_name = edit_name.value.strip()
            new_amount_str = edit_amount.value.strip()
            try:
                new_amount = float(new_amount_str)
                if new_amount <= 0:
                    raise ValueError()
            except ValueError:
                page.snack_bar = Text("Некорректная сумма")
                page.snack_bar.open = True
                page.update()
                return

            expenses[index] = {"name": new_name, "amount": new_amount}
            edit_dialog.open = False
            refresh_list()

        edit_dialog.title = Text("Редактировать расход")
        edit_dialog.content = Column([edit_name, edit_amount], tight=True)
        edit_dialog.actions = [
            ElevatedButton(text="Сохранить", on_click=save_edit),
            ElevatedButton(text="Отмена", on_click=lambda e: close_dialog())
        ]
        edit_dialog.open = True
        page.dialog = edit_dialog
        page.update()

    def close_dialog():
        edit_dialog.open = False
        page.update()

    # Кнопка добавления
    add_button = ElevatedButton(text="Добавить расход", on_click=add_expense)

    # Интерфейс
    page.add(
        name_input,
        amount_input,
        add_button,
        Text("Список расходов:"),
        expenses_list,
        total_text
    )

flet.app(target=main)

