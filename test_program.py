import flet as ft
import time 
from os import path 
import os

def main(page: ft.Page):
    time.sleep(2)
    page.add(ft.Text(os.listdir()))
    time.sleep(2)
    assets = os.listdir(path.abspath(path.join(path.dirname(__file__), 'assets')))
    page.add(ft.Text(assets))

    page.update()

ft.app(target=main,assets_dir="assets")