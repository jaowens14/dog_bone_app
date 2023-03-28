import flet as ft
import os 
import stat
import time
import datetime
import pandas as pd
from PIL import ImageGrab
import json
from parse_html import parse_report
from color_map import grade_dog_bone
from helper_functions import create_build_output_directory
from google_drive_autho import upload_build
import shutil

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

from ../components/dog_gone_app import DogBoneApp






class Build(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.number =               ft.TextField(label='Build Number',         value='0000', expand=4, on_blur=self.change_build_number)
        self.elongation_threshold = ft.TextField(label='Elongation Threshold', value='', expand=2, read_only=True)
        self.stress_threshold =     ft.TextField(label='Stress Threshold',     value='', expand=2, read_only=True)
        self.previous_number = '0000'
        
        self.material = ft.Dropdown(
            label="Build Material",
            options=[
                ft.dropdown.Option("PA12"),
                ft.dropdown.Option("PA11"),
                ft.dropdown.Option("M95"),
                ft.dropdown.Option("M88"),
            ],
            on_change=self.select_material,
            expand=2
        )


    def build(self):
        self.header = ft.Column(
            controls=[
                ft.Row(
                    alignment=ft.alignment.center,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10,
                    controls=[
                        self.number,
                        self.material,
                    ],
                ),
            ft.Divider(thickness=5, color=ft.colors.BLUE_GREY)
            ],
        )
        return self.header

    def change_build_number(self, e):
        print(self.number.value)
        self.update()

    def select_material(self, e):
        material_thresholds = {
        'M95' :  {"STRESS" : {"STD":3.0, "AVE": 20.0}, "ELONGATION" : {"STD":3.0, "AVE":20.0}},
        'M88' :  {"STRESS" : {"STD":3.0, "AVE": 20.0}, "ELONGATION" : {"STD":3.0, "AVE":20.0}},
        'PA12' : {"STRESS" : {"STD":3.0, "AVE": 20.0}, "ELONGATION" : {"STD":3.0, "AVE":20.0}},
        'PA11' : {"STRESS" : {"STD":3.0, "AVE": 20.0}, "ELONGATION" : {"STD":3.0, "AVE":20.0}},
        }
        self.stress_threshold.value  = material_thresholds[self.material.value]['STRESS']['AVE']
        self.elongation_threshold.value = material_thresholds[self.material.value]['ELONGATION']['AVE']
        self.update()
        


class DogBone(ft.UserControl):
    def __init__(self, delete_func):
        super().__init__()
        self.entry_number=ft.TextButton(text='',                         expand=2)
        self.file_path =  ft.TextField(label='File',           value='', expand=30, read_only=True, bgcolor=ft.colors.BLUE_GREY_50)
        self.number =     ft.TextField(label='Number',         value='', expand=15)
        self.length =     ft.TextField(label='Length [mm]',    value='', expand=25)
        self.width =      ft.TextField(label='Width [mm]',     value='', expand=25)
        self.thickness =  ft.TextField(label='Thickness [mm]', value='', expand=25)
        self.elongation = ft.TextField(label='Elongation [%]', value='', expand=25, read_only=True, bgcolor=ft.colors.BLUE_GREY_50)
        self.force      = ft.TextField(label='Force [N]' ,     value='', expand=25, read_only=True, bgcolor=ft.colors.BLUE_GREY_50)
        self.stress =     ft.TextField(label='Stress [MPA]',   value='', expand=25, read_only=True, bgcolor=ft.colors.BLUE_GREY_50)
        self.delete_func = delete_func
        self.delete =     ft.IconButton(ft.icons.DELETE, on_click=self.delete_dog_bone)
        self.lock =       ft.IconButton(ft.icons.LOCK_OPEN_OUTLINED, on_click=self.lock_dog_bone)
        self.unlock =     ft.IconButton(ft.icons.LOCK_OUTLINED, visible=False, on_click=self.unlock_dog_bone)

    def build(self):
        self.view = ft.Row(
            alignment=ft.alignment.center,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
            controls=[
                #self.entry_number,
                self.file_path, 
                self.number, 
                self.length, 
                self.width, 
                self.thickness, 
                self.elongation, 
                self.force,
                #self.stress,
                self.lock,
                self.unlock,
                self.delete,
                ],
        )
        return self.view
    
    #########################################################################
    # data processing area

    def process_dog_bone(self, e, dog_bone_number, material, data_file_path):
        
        length    = self.length.value
        width     = self.width.value
        thickness = self.thickness.value
        cross_sectional_area = float(thickness)*float(width)
        # load the data
        os.chmod(data_file_path, stat.S_IRWXU)
        # open the file
        report = open(data_file_path, 'r')
        # get the data out of the html
        sample_data = parse_report(report)
        # REMEMBER the columns are : columns=['Reading Number', 'Load [N]', 'Travel [mm]', 'Time [sec]'])
        sample_data['Load [N]'] = -sample_data['Load [N]'].astype(float)
        sample_data['Travel [mm]'] = sample_data['Travel [mm]'].astype(float)
        max_load = sample_data['Load [N]'].max()
        travel_at_max_load = max(sample_data.loc[sample_data["Load [N]"] == max_load, 'Travel [mm]'])
        percent_elongation = round(((travel_at_max_load/25) * 100),2)

        #engineering_stress = round(max_load/cross_sectional_area, 4)
        max_force = max_load
        self.force.value = max_force

        self.elongation.value = percent_elongation
        # calculate the values, results
        # score the results
        # write results to fields
        # write scores to colors
        # update dog bone
        print("WE made it right before grade")
        colors = grade_dog_bone(material, dog_bone_number, length, width, thickness, percent_elongation, max_force)
        print("GRADE")
        print(colors)
        self.length.bgcolor = colors['Length']
        self.width.bgcolor = colors['Width']
        self.thickness.bgcolor = colors['Thickness']
        self.force.bgcolor = colors['Force']
        self.elongation.bgcolor = colors['Elongation']
        print(colors)

        self.update()
            
        print("processed dog bones")
    #########################################################################
    

    def delete_dog_bone(self, e):
        self.delete_func(self)

    def lock_dog_bone(self, e):
        self.lock.visible = False
        self.unlock.visible = True
        self.file_path.read_only = True
        self.number.read_only    = True
        self.length.read_only    = True
        self.width.read_only     = True
        self.thickness.read_only = True
        self.delete.visible      = False
        self.update()

    def unlock_dog_bone(self, e):
        self.unlock.visible = False
        self.lock.visible = True
        self.file_path.read_only = True
        self.number.read_only    = False
        self.length.read_only    = False
        self.width.read_only     = False
        self.thickness.read_only = False
        self.delete.visible      = True
        self.update()


class DogBoneApp(ft.UserControl):
    def __init__(self):
        super().__init__()
        
    def build(self):
        self.report = {}
        self.progress_bar = ft.ProgressBar(visible=False)
        self.t = '' # time stamp
        self.message = ft.TextField(label="Message", value='', read_only=True, expand=2)
        self.notes   = ft.TextField(label="Notes", value='', expand=3)

        self.header = Build()
        self.dog_bones = ft.Column()
        self.get_directory_dialog = ft.FilePicker(on_result=self.get_directory_result)

        self.clear_data_button = ft.FloatingActionButton(text='Clear All Data', expand=1, on_click=self.show_banner, bgcolor=ft.colors.RED_300)
        self.banner = ft.Banner(
        open=False,
        bgcolor=ft.colors.AMBER_100,
        leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.AMBER, size=40),
        content=ft.Text(
            "Are you sure you want to clear all data? Please confirm you have saved the build."
        ),
        actions=[
            ft.TextButton("Clear All Data", on_click=self.clear_all_data),
            ft.TextButton("Cancel", on_click=self.hide_banner),
        ],
    )




        return ft.Column(
            spacing=10,
            width=1600,
            controls=[
                self.header,
                ft.Row(
                    controls=[
                        ft.FloatingActionButton(icon=ft.icons.ADD,         on_click=self.add_clicked,  text="Add A Dog Bone", expand=1),
                        ft.FloatingActionButton(icon=ft.icons.FOLDER_OPEN, on_click=lambda _: self.get_directory_dialog.get_directory_path(), text="Select Build Directory", expand=1),
                        self.message,
                    ],
                ),
                self.dog_bones,
                ft.Divider(thickness=5, color=ft.colors.BLUE_GREY),
                self.progress_bar,
                ft.Row(
                    controls=[
                        ft.FloatingActionButton(icon=ft.icons.CREATE, text="Create Build Report", expand=2, bgcolor=ft.colors.GREEN_300, on_click=self.save_build),
                        #ft.FloatingActionButton(icon=ft.icons.CREATE, text="print stuff", expand=1, on_click=self.print_stuff, bgcolor=ft.colors.GREEN_300),
                        self.notes,
                        self.clear_data_button,
                        self.banner,
                        self.get_directory_dialog,
                    ],
                ),
            ],
        )

    def show_banner(self, e):
        print("show banner")
        self.banner.open = True
        self.update()
    def hide_banner(self, e):
        print("hide banner")
        self.banner.open = False
        self.update()

    def clear_all_data(self, e):
        self.header.material.value = ''
        self.header.number.value = '0000'
        self.dog_bones.controls = []
        self.banner.open = False
        self.message.value = ''
        self.header.update()
        self.dog_bones.update()
        self.update()
        print("clear all data")


    def print_stuff(self, e):
        self.message.bgcolor = ft.colors.AMBER_300
        self.update()
        time.sleep(1.0)

        self.message.value = str(os.listdir('.\\'))
        self.update()
        time.sleep(1.0)


    def add_clicked(self, e):
        new_dog_bone = DogBone(self.remove_dog_bone)
        new_dog_bone.entry_number.text = str(len(self.dog_bones.controls)+1)
        self.dog_bones.controls.append(new_dog_bone)
        self.update()

    def remove_dog_bone(self, dog_bone):
        self.dog_bones.controls.remove(dog_bone)
        self.update()

    def save_build(self, e):
        # all of the dog bone unlocks need to be visible true in order to save a build
        if all([db.unlock.visible for db in self.dog_bones.controls]) == True:
            #self.message.value = "* Build Report Saved *"
            #self.message.bgcolor = ft.colors.GREEN_400
            #self.update()
            self.t = datetime.datetime.fromtimestamp(time.time()).strftime('%m-%d-%Y')
            self.build_output_path = create_build_output_directory(self.header.number.value)
            self.capture_build_screenshot(e)
            self.create_json_from_data(e)
            self.save_html_files(e)
            time.sleep(0.1)
            self.progress_bar.visible=True
            self.message.value = "Uploading Build Files. Please Wait."
            self.message.bgcolor = ft.colors.AMBER_300
            self.update()
            self.upload_build_directory(e)
            self.message.value = "Upload Complete."
            self.message.bgcolor = ft.colors.GREEN_300
            self.progress_bar.visible=False
            self.update()
        

        else:
            self.message.value = "Please Lock All Dog Bones"
            self.message.bgcolor = ft.colors.AMBER_300
            self.update()


    def capture_build_screenshot(self, e):
        print("HERE")
        self.page.window_maximized = True
        self.page.update()
        time.sleep(0.5)
        screenshot = ImageGrab.grab()
        self.page.window_maximized = False
        self.page.update()
        reportpath = os.path.join(self.build_output_path, str(self.header.number.value)+"_Report_"+str(self.t)+'.png')
        screenshot.save(reportpath, 'PNG')


    def create_json_from_data(self, e):
        try:
            self.report['BUILD'] = {
                "NUMBER": self.header.number.value,
                #"ELONGATION THRESHOLD": self.header.elongation_threshold.value,
                #"STRESS THRESHOLD": self.header.stress_threshold.value,
                "MATERIAL": self.header.material.value,
                "NOTES": self.notes.value,
                }
            dogbones = []
            for db in self.dog_bones.controls:
                dogbone = {
                    "File" :      db.file_path.value, 
                    "Number":     db.number.value,
                    "Length":     db.length.value,
                    "Width":      db.width.value,
                    "Thickness":  db.thickness.value,
                    "Elongation": db.elongation.value,
                    "Load":       db.force.value,
                    }
                dogbones.append(dogbone)
            self.report['DOG_BONES'] = dogbones
            json_output_file = os.path.join(self.build_output_path, str(self.header.number.value)+"_Report_"+str(self.t)+'.json')
            print(json_output_file)
            jf = open(json_output_file, 'x')
            json.dump(self.report, jf, indent=4)
            print(self.report)
            print("Create json")
        except FileExistsError:
            self.message.bgcolor = ft.colors.AMBER_300
            self.message.value = "Looks like some of those files already exist. Check your dog_bone_app_local_output directory."
            self.update()


    def save_html_files(self, e):
        for db in self.dog_bones.controls:
            src = os.path.join(self.build_directory, db.file_path.value)
            dst = os.path.join(self.build_output_path, db.file_path.value)
            shutil.copyfile(src, dst)
        print("save html files")

    def upload_build_directory(self, e):
        try:
            upload_build(self.build_output_path)
        except Exception as e:
            self.message.bgcolor = ft.colors.AMBER_300
            self.message.value = "UPLOAD ERROR"+str(e)
            self.update()        
        print("upload files")



    def get_directory_result(self, e: ft.FilePickerResultEvent):
        if len(self.dog_bones.controls) == 0:
            self.message.value = "Please Add Some Dog Bones Before Selecting Build"
            self.message.bgcolor = ft.colors.AMBER_300
            self.update()
        elif self.header.number.value != os.path.basename(os.path.normpath(e.path)):
            self.message.value = "The Selected Directory Does Not Match the Build Number"
            self.message.bgcolor = ft.colors.AMBER_300
            print(os.path.basename(os.path.normpath(e.path)))
            self.update()
        elif all([False for db in self.dog_bones.controls if db.number.value !='']):
            self.message.value = "Make sure to enter the dog bone numbers"
            self.message.bgcolor = ft.colors.AMBER_300
            self.update()
        else:
            if all([db.unlock.visible for db in self.dog_bones.controls]) == True:
                try:
                    # for every file in the folder, do stuff
                    build_number = os.path.basename(os.path.normpath(e.path))
                    for db in self.dog_bones.controls:
                        dog_bone_number = db.number.value
                        self.data_file_path = os.path.join(e.path, build_number+'_'+dog_bone_number+'.html')
                        assert os.path.exists(self.data_file_path), "Valid path expected"
                        print('data file path')
                        print(self.data_file_path)
                        db.file_path.value = build_number+'_'+dog_bone_number+'.html'
                        self.build_directory = e.path
                        db.process_dog_bone(e, db.number.value, self.header.material.value, self.data_file_path)
                        self.message.bgcolor = ft.colors.GREEN_300
                        self.message.value = "Loaded and processed dog bones"
                        self.update()
                
                except AssertionError:
                    db.file_path.value = ''
                    self.message.bgcolor = ft.colors.AMBER_300
                    self.message.value = "Looks like you are missing a dog bone file"
                    self.message.update()

                except ValueError:
                    self.message.bgcolor = ft.colors.AMBER_300
                    self.message.value = "It looks like some values were left blank"
                    self.update()

                except IndexError:
                    self.message.bgcolor = ft.colors.AMBER_300
                    self.message.value = "Different Number of Dog Bones vs Dog Bone Files"
                    self.update()
                except KeyError:
                    self.message.bgcolor = ft.colors.AMBER_300
                    self.message.value = "Make Sure to Select a Material"
                    self.update()
                
                except FileNotFoundError:
                    self.message.bgcolor = ft.colors.AMBER_300
                    self.message.value = "Looks Like There Was an Error Loading the Files. Try Again"
                    self.update()

            else:
                self.message.value = "Please Lock All Dog Bones Before Selecting Build"
                self.message.bgcolor = ft.colors.AMBER_300
                self.update()


def main(page: ft.Page):
    page.title = "Dog Bone App"
    page.scroll = ft.ScrollMode.ALWAYS
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.update()

    # create application instance
    dog_bone_app = DogBoneApp()

    # add application's root control to the page
    page.add(dog_bone_app)

if __name__ == "__main__":
    print("aaa")
    # ft.app(target=main,assets_dir="assets")