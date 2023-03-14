import flet as ft
import time 
import os

def main(page: ft.Page):
    time.sleep(2)
    page.add(ft.Text(os.listdir()))
    time.sleep(2)
    page.add(ft.Text(os.listdir("assets")))
    page.update()

ft.app(target=main,assets_dir="assets")