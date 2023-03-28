import flet as ft
from .build_info import BuildInfo
import time
import os
from dog_bone import DogBone
import datetime
from PIL import ImageGrab
from components.build_info import create_build_output_directory
import json
import shutil
from utils.google_drive_autho import upload_build


class DogBoneApp(ft.UserControl):
    def __init__(self):
        super().__init__()

    def show_banner(self, e):
        print("show banner")
        self.banner.open = True
        self.update()

    def hide_banner(self, e):
        print("hide banner")
        self.banner.open = False
        self.update()

    def clear_all_data(self, e):
        print("clear all data")
        self.header.material.value = ''
        self.header.number.value = '0000'
        self.dog_bones.controls = []
        self.banner.open = False
        self.message.value = ''
        self.header.update()
        self.dog_bones.update()
        self.update()

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
        print("screenshot")
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
        
    def build(self):
        self.report = {}
        self.progress_bar = ft.ProgressBar(visible=False)
        self.t = ''
        self.message = ft.TextField(
            label="Message", 
            value='', 
            read_only=True, 
            expand=2
        )
        self.notes = ft.TextField(
            label="Notes", 
            value='', 
            expand=3
        )
        self.header = BuildInfo()
        self.dog_bones = ft.Column()
        self.get_directory_dialog = ft.FilePicker(on_result=self.get_directory_result)

        self.clear_data_button = ft.FloatingActionButton(
            text='Clear All Data', 
            expand=1, 
            on_click=self.show_banner, 
            bgcolor=ft.colors.RED_300
        )
        self.banner = ft.Banner(
            open=False,
            bgcolor=ft.colors.AMBER_100,
            leading=ft.Icon(
                ft.icons.WARNING_AMBER_ROUNDED, 
                color=ft.colors.AMBER, 
                size=40
            ),
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

    
    

    


    


    

    

    


  


    
