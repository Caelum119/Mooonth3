import flet as ft
from database import Database

def main(page: ft.Page):
    page.title = "Трекер расходов"
    page.window_width = 1024
    page.data = 0  # для хранения id при редактировании

    db = Database("expenses.db")
    db.create_table()

    def get_rows():
        rows = []
        for exp in db.all_expenses():
            rows.append(
                ft.Row(
                    controls=[
                        ft.Text(f"{exp[1]} сом", size=28),
                        ft.Text(f"Категория: {exp[2]}", size=20, color=ft.Colors.BLUE),
                        ft.IconButton(
                            icon=ft.Icons.EDIT,
                            icon_color=ft.Colors.GREEN,
                            on_click=open_edit_modal,
                            data=exp[0],
                        ),
                        ft.IconButton(
                            icon=ft.Icons.DELETE,
                            icon_color=ft.Colors.RED,
                            on_click=delete_expense,
                            data=exp[0],
                        ),
                    ]
                )
            )
        return rows

    def refresh():
        expense_list.controls = get_rows()
        total_text.value = f"Общая сумма: {db.total_sum()} сом"
        amount_input.value = ""
        category_input.value = ""
        page.update()

    def add_expense(e):
        if amount_input.value and category_input.value:
            db.add_expense(int(amount_input.value), category_input.value)
            refresh()

    def delete_expense(e):
        db.delete_expense(e.control.data)
        refresh()

    def open_edit_modal(e):
        page.data = e.control.data
        exp = db.get_expense(page.data)
        amount_input.value = str(exp[1])
        category_input.value = exp[2]
        page.dialog = edit_modal
        edit_modal.open = True
        page.update()

    def close_modal(e):
        edit_modal.open = False
        page.update()

    def update_expense(e):
        db.update_expense(page.data, int(amount_input.value), category_input.value)
        edit_modal.open = False
        refresh()

    # UI
    amount_input = ft.TextField(label="Сумма", width=200)
    category_input = ft.TextField(label="Категория", width=200)
    add_btn = ft.ElevatedButton("Добавить", on_click=add_expense)
    total_text = ft.Text(f"Общая сумма: {db.total_sum()} сом", size=28)
    expense_list = ft.Column(controls=get_rows(), scroll="auto", expand=True)

    edit_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Редактировать расход"),
        content=ft.Column([amount_input, category_input]),
        actions=[
            ft.ElevatedButton("Сохранить", on_click=update_expense),
            ft.TextButton("Отменить", on_click=close_modal)
        ]
    )

    page.add(
        ft.Text("Мои расходы", size=32),
        ft.Row([amount_input, category_input, add_btn]),
        total_text,
        expense_list
    )

ft.app(main)
