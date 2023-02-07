import flet as ft
import time 
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


def main(page: ft.Page):
    page.title = "Dog Bone Application"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    txt_number = ft.TextField(value="0", text_align=ft.TextAlign.RIGHT, width=100)
    file_path = ft.TextField(value=" ", text_align=ft.TextAlign.RIGHT, width=500 )  # fill all the space
    
    indicator = ft.Container(
        width=150,
        height=150,
        bgcolor="blue",
        border_radius=10,
        animate_opacity=300,
    )

    def animate_indicator(e):
        indicator.opacity = 0 if indicator.opacity == 1 else 1
        indicator.update()

    class ExampleHandler(FileSystemEventHandler):
        def on_created(self, event): # when file is created
            # do something, eg. call your function to process the image
            print ("Got event for file %s" % event.src_path)
            print("process detected file")
            print("send result to FRONT END")
            file_path.value = event.src_path
            animate_indicator(event)
            page.update()

    observer = Observer()
    event_handler = ExampleHandler() # create event handler

    def system_file_changes():
        # set observer to use created handler in directory
        observer.schedule(event_handler, path='.')
        observer.start()
        # sleep until keyboard interrupt, then stop + rejoin the observer
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()


    def minus_click(e):
        txt_number.value = str(int(txt_number.value) - 1)
        page.update()

    def plus_click(e):
        txt_number.value = str(int(txt_number.value) + 1)
        page.update()


    page.add(
        ft.Row(
            [
                ft.IconButton(ft.icons.REMOVE, on_click=minus_click),
                txt_number,
                ft.IconButton(ft.icons.ADD, on_click=plus_click),
                file_path,
                indicator
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )

    system_file_changes()

ft.app(target=main)