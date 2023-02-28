import flet as ft
import time 
import os
import stat
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pandas as pd
import numpy as np
from parse_html import parse_report

# TODO add example header to error message
# TODO input threshold values
# TODO add multi-color rules
# TODO add a clear results button/function

# git add .
# git commit -m "commit here"
# git push -u origin master

# example of sample header:
# {'BUILD NUMBER': '00000', 'MATERIAL': 'PA12', 'DOG BONE NUMBER': '5', 'LENGTH': '75.00', 'WIDTH': '4.0', 'THICKNESS': '2.0'}
# stress in MPA and 
thresholds = {
    'M95' :  {"ENGINEERING STRESS" : 5.1, "PERCENT ELONGATION" : 15},
    'M88' :  {"ENGINEERING STRESS" : 6.2, "PERCENT ELONGATION" : 15},
    'PA12' : {"ENGINEERING STRESS" : 7.3, "PERCENT ELONGATION" : 15},
    'PA11' : {"ENGINEERING STRESS" : 8.4, "PERCENT ELONGATION" : 15},
}

w = 350



class Dogbone(UserControl):
    def __init__(self, dog_bone_number, ):
        super().__init__()



def main(page: ft.Page):
    page.title = "Dog Bone Application"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    file_path_field = ft.TextField(value=" ", text_align=ft.TextAlign.LEFT, width=900, height=50, text_size=12)  # fill all the space
    
    thresholds_container = ft.Container(
        content=ft.Text("THRESHOLDS : ----", size=18),
        alignment=ft.alignment.center,
        width=w*3+20,
        height=50,
        bgcolor=ft.colors.BLUE_GREY,
        border_radius=10,
        animate_opacity=300,
    )

    strength_container = ft.Container(
        content=ft.Text("MAXIMUM LOAD [N] : ----", size=18),
        alignment=ft.alignment.center,
        width=w,
        height=50,
        bgcolor=ft.colors.BLUE_GREY,
        border_radius=10,
        animate_opacity=300,
    )

    stress_container = ft.Container(
        content=ft.Text("ENGINEERING STRESS [MPA] : ----", size=18),
        alignment=ft.alignment.center,
        width=w,
        height=50,
        bgcolor=ft.colors.BLUE_GREY,
        border_radius=10,
        animate_opacity=300,
    )

    build_container = ft.Container(
        content=ft.Text("BUILD : ------", size=18),
        alignment=ft.alignment.center,
        width=w,
        height=50,
        bgcolor=ft.colors.BLUE_GREY,
        border_radius=10,
        animate_opacity=300,
    )

    material_container = ft.Container(
        content=ft.Text("MATERIAL : ----", size=18),
        alignment=ft.alignment.center,
        width=w,
        height=50,
        bgcolor=ft.colors.BLUE_GREY,
        border_radius=10,
        animate_opacity=300,
    )

    dog_bone_number_container = ft.Container(
        content=ft.Text("DOG BONE NUMBER : --", size=18),
        alignment=ft.alignment.center,
        width=w,
        height=50,
        bgcolor=ft.colors.BLUE_GREY,
        border_radius=10,
        animate_opacity=300,
    )

    length_container = ft.Container(
        content=ft.Text("LENGTH : ----", size=18),
        alignment=ft.alignment.center,
        width=w,
        height=50,
        bgcolor=ft.colors.BLUE_GREY,
        border_radius=10,
        animate_opacity=300,
    )

    width_container = ft.Container(
        content=ft.Text("WIDTH : ----", size=18),
        alignment=ft.alignment.center,
        width=w,
        height=50,
        bgcolor=ft.colors.BLUE_GREY,
        border_radius=10,
        animate_opacity=300,
    )

    thickness_container = ft.Container(
        content=ft.Text("THICKNESS : ----", size=18),
        alignment=ft.alignment.center,
        width=w,
        height=50,
        bgcolor=ft.colors.BLUE_GREY,
        border_radius=10,
        animate_opacity=300,
    )
    elongation_container = ft.Container(
        content=ft.Text("PERCENT ELONGATION [%]: ----", size=18),
        alignment=ft.alignment.center,
        width=w,
        height=50,
        bgcolor=ft.colors.BLUE_GREY,
        border_radius=10,
        animate_opacity=300,
    )

    def process_file(data_file_path):
        try:
            time.sleep(1)
            os.chmod(data_file_path, stat.S_IRWXO)
            # open the file
            report = open(data_file_path, 'r')
            # parse the file
            sample_header, sample_data = parse_report(report)
            stress_threshold = thresholds[sample_header['MATERIAL']]['ENGINEERING STRESS']
            elongation_threshold = thresholds[sample_header['MATERIAL']]['PERCENT ELONGATION']

            print(stress_threshold)
            print(elongation_threshold)
            # {'BUILD NUMBER': '00000', 'MATERIAL': 'PA12', 'DOG BONE NUMBER': '5', 'LENGTH': '75.00', 'WIDTH': '4.0', 'THICKNESS': '2.0'}
            thresholds_container.content =      ft.Text(str(sample_header['MATERIAL'])+" THRESHOLDS : "+str(thresholds[sample_header['MATERIAL']]),text_align=ft.alignment.center, size=18)
            build_container.content =           ft.Text("BUILD : "+sample_header['BUILD NUMBER'], text_align=ft.alignment.center, size=18)
            material_container.content =        ft.Text("MATERIAL : "+sample_header['MATERIAL'], text_align=ft.alignment.center, size=18)
            dog_bone_number_container.content = ft.Text("DOG BONE NUMBER : "+sample_header['DOG BONE NUMBER'], text_align=ft.alignment.center, size=18)
            length_container.content =          ft.Text("LENGTH : "+sample_header['LENGTH'], text_align=ft.alignment.center, size=18)
            width_container.content =           ft.Text("WIDTH : "+sample_header['WIDTH'], text_align=ft.alignment.center, size=18)
            thickness_container.content =       ft.Text("THICKNESS : "+sample_header['THICKNESS'], text_align=ft.alignment.center, size=18)
            # convert strings to numbers and then the mm to meters for stress calc
            cross_section_area = float(sample_header['THICKNESS'])*float(sample_header['WIDTH'])
            sample_data['Load [N]'] = -sample_data['Load [N]'].astype(float)
            sample_data['Travel [mm]'] = sample_data['Travel [mm]'].astype(float)
            max_load = sample_data['Load [N]'].max()
            travel_at_max_load = max(sample_data.loc[sample_data["Load [N]"] == max_load, 'Travel [mm]'])
            percent_elongation = round(((travel_at_max_load/25) * 100),2)
            engineering_stress = round(max_load/cross_section_area, 4)
            elongation_container.content = ft.Text("PERCENT ELONGATION [%]: " + str(percent_elongation), text_align=ft.alignment.center, size=18)
            strength_container.content = ft.Text("MAXIMUM LOAD [N] : " + str(max_load), text_align=ft.alignment.center, size=18)
            stress_container.content = ft.Text("ENGINEERING STRESS [MPA] : " + str(engineering_stress), text_align=ft.alignment.center, size=18)
            file_path_field.value = "Selected file: "+str(data_file_path)


            if engineering_stress < stress_threshold:
                stress_container.bgcolor = ft.colors.RED
            else:
                stress_container.bgcolor = ft.colors.BLUE_GREY
            
            
            if percent_elongation < elongation_threshold:
                elongation_container.bgcolor = ft.colors.RED
            else:
                elongation_container.bgcolor = ft.colors.BLUE_GREY




        except Exception as e:
            print("Error in process_file function")
            print(e)
            file_path_field.value = "ERROR: process_file function, Check header format"
            file_path_field.bgcolor = ft.colors.RED
            page.update()



    class ExampleHandler(FileSystemEventHandler):
        def on_created(self, event): # when file is created
            try:
                file_path_field.value = ""
                file_path_field.bgcolor = ft.colors.WHITE
                page.update()
                # do something, eg. call your function to process the image
                print ("Got event for file %s" % event.src_path)
                process_file(event.src_path)
                page.update()
            except Exception as e:
                print("Error in on_created function")
                print(e)
                file_path_field.value = "ERROR: on_created function, Check header format"
                file_path_field.bgcolor = ft.colors.RED
                page.update()



    # watch dog stuff
    observer = Observer()
    event_handler = ExampleHandler() # create event handler

    def system_file_changes():
        try:
            # set observer to use created handler in directory
            file_path_field.value = ""
            file_path_field.bgcolor = ft.colors.WHITE
            page.update()
            observer.schedule(event_handler, path='.')
            observer.start()
            # sleep until keyboard interrupt, then stop + rejoin the observer
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                observer.stop()
            observer.join()
        except Exception as e:
            print("Error in system_file_changes function")
            print(e)
            file_path_field.value = "ERROR: system_file_changes function, check watchdog"
            file_path_field.bgcolor = ft.colors.RED
            page.update()


    # reset and file picker
    def on_dialog_result(e: ft.FilePickerResultEvent):
        try:
            file_path_field.value = ""
            file_path_field.bgcolor = ft.colors.WHITE
            page.update()
            print("Selected files:", e.files)
            file_name = e.files[0].name
            file_path = e.files[0].path
            process_file(file_path)
            page.update()
        except Exception as e:
            print("Error in on_dialog_result function")
            print(e)
            file_path_field.value = "ERROR: on_dialog_result function, check file picker"
            file_path_field.bgcolor = ft.colors.RED
            page.update()
        


    file_picker = ft.FilePicker(on_result=on_dialog_result)
    page.overlay.append(file_picker)
    page.update()

    page.add(
        # file row
        ft.Row(
            [
                file_path_field, ft.OutlinedButton("SELECT REPORT", on_click=lambda _: file_picker.pick_files(allow_multiple=False))

            ],
            alignment=ft.MainAxisAlignment.START,
        ),

        # header row
        ft.Row(
            [
                # {'BUILD NUMBER': '00000', 'MATERIAL': 'PA12', 'DOG BONE NUMBER': '5', 'LENGTH': '75.00', 'WIDTH': '4.0', 'THICKNESS': '2.0'}

                build_container, material_container, dog_bone_number_container
            ],
            alignment=ft.MainAxisAlignment.START
        ),

        # measurements row
        ft.Row(
            [
                length_container, width_container, thickness_container
            ],
            alignment=ft.MainAxisAlignment.START
        ),

        # properties row
        ft.Row(
            [
                strength_container, elongation_container, stress_container
            ],
            alignment=ft.MainAxisAlignment.START
        ),
        # thresholds row
        ft.Row(
            [
                thresholds_container
            ], 
            alignment=ft.MainAxisAlignment.START
        )
    )

    system_file_changes()

ft.app(target=main)

