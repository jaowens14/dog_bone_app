import flet as ft
import time 
import os
import stat
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pandas as pd
import numpy as np
from parse_html import parse_report


# git add .
# git commit -m "commit here"
# git push -u origin master


strength_threshold = 600 #in newtons
elongation_threshold = 30 # in percent

def main(page: ft.Page):
    page.title = "Dog Bone Application"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    file_path = ft.TextField(value=" ", text_align=ft.TextAlign.LEFT, width=750, height=50, text_size=12)  # fill all the space
    
    strength_indicator = ft.Container(
        content=ft.Text(""),
        width=150,
        height=50,
        bgcolor="Blue",
        border_radius=10,
        animate_opacity=300,
    )

    elongation_indicator = ft.Container(
        content=ft.Text(""),
        width=150,
        height=50,
        bgcolor="Blue",
        border_radius=10,
        animate_opacity=300,
    )


    class ExampleHandler(FileSystemEventHandler):
        def on_created(self, event): # when file is created
            # do something, eg. call your function to process the image
            print ("Got event for file %s" % event.src_path)

            # give the correct permissions to open the file.
            os.chmod(event.src_path, stat.S_IRWXO)

            # open the file
            report = open(event.src_path, 'r')
            
            # parse the file
            sample_header, sample_data = parse_report(report)
            
            file_path.value = str(sample_header)

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



    page.add(
        # file row
        ft.Row(
            [
                file_path,
            ],
            alignment=ft.MainAxisAlignment.START,
        ),

        # header row
        ft.Row(
            [
                strength_indicator, elongation_indicator
            ],
            alignment=ft.MainAxisAlignment.START
        ),

        # measurements row
        ft.Row(
            [
                strength_indicator, elongation_indicator
            ],
            alignment=ft.MainAxisAlignment.START
        ),

        # properties row
        ft.Row(
            [
                strength_indicator, elongation_indicator,
            ],
            alignment=ft.MainAxisAlignment.START
        )
    )

    system_file_changes()

ft.app(target=main)

