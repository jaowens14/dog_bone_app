import flet as ft

def main(page: ft.page):
    page.add(ft.Text(value="hello world"))

ft.app(target=main)