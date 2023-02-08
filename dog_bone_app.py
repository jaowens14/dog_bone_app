import flet as ft
import time 
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pandas as pd
import numpy as np

strength_threshold = 600 #in newtons
elongation_threshold = 30 # in percent

def main(page: ft.Page):
    page.title = "Dog Bone Application"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    file_path = ft.TextField(value=" ", text_align=ft.TextAlign.RIGHT, width=500, height=50)  # fill all the space
    selected_file_text = ft.Text(value="Selected File: ", size=18)

    strength_threshold_text = ft.Text(value="Peak Strength Minimum: "+str(strength_threshold)+" N", size=18)
    elongation_threshold_text = ft.Text(value="Elongation Minimum: "+str(elongation_threshold)+" %", size=18)

    sample_strength_text = ft.Text(value="Sample Strength: ", size=18)
    sample_elongation_text = ft.Text(value="Sample Elongation: ", size=18)

    
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

            test_data = pd.read_csv(event.src_path).to_numpy()
            sample_strength = np.max(test_data[:,0])
            sample_elongation = np.max(test_data[:,1])

            if sample_strength < strength_threshold:
                # set indicator property color to red
                # set indicator text to low strength
                strength_indicator.bgcolor = "Red"
                strength_indicator.content = ft.Text("WARNING: LOW STRENGTH", size=12)
                strength_indicator.update()
                file_path.value = event.src_path
                page.update()
            else:
                strength_indicator.bgcolor = "Green"
                strength_indicator.content = ft.Text("ACCEPTABLE STRENGTH", size=12)
                strength_indicator.update()
                file_path.value = event.src_path
                page.update()

            if sample_elongation < elongation_threshold:
                elongation_indicator.bgcolor = "Red"
                elongation_indicator.content = ft.Text("WARNING: LOW ELONGATION", size=12)
                elongation_indicator.update()
                file_path.value = event.src_path
                page.update()
            else:
                elongation_indicator.bgcolor = "Green"
                elongation_indicator.content = ft.Text("ACCEPTABLE ENLONGATION", size=12)
                elongation_indicator.update()
                file_path.value = event.src_path
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
        ft.Row(
            [
                strength_threshold_text,
                elongation_threshold_text
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
    
        ft.Row(
            [
                selected_file_text, file_path,

            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),

        ft.Row(
            [
               sample_strength_text, strength_indicator,
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),

        ft.Row(
            [
               sample_elongation_text, elongation_indicator,
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )

    system_file_changes()

ft.app(target=main)