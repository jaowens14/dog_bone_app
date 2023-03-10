import flet as ft
import os 
import stat
from parse_html import parse_report
import pandas as pd
from PIL import ImageGrab
import time

from color_map import value_to_color


class Build(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.number =               ft.TextField(label='Build Number',         value='0000', expand=2, on_blur=self.change_build_number)
        self.elongation_threshold = ft.TextField(label='Elongation Threshold', value='', expand=1, read_only=True)
        self.stress_threshold =     ft.TextField(label='Stress Threshold',     value='', expand=1, read_only=True)
        self.previous_number = '0000'

        ''' I took out the banner because it didn't seem to be that helpful
        self.banner = ft.Banner(
            open=False,
            bgcolor=ft.colors.AMBER_100,
            leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.AMBER, size=40),
            content=ft.Text(
                "Oops, looks like you are trying to change the build number. What would you like to do?"
            ),
            actions=[
                ft.TextButton("Change Build Number", on_click=self.change_number),
                ft.TextButton("Ignore", on_click=self.ignore),
            ],
    )
    '''
        
        self.material = ft.Dropdown(
            label="Build Material",
            options=[
                ft.dropdown.Option("PA12"),
                ft.dropdown.Option("PA11"),
                ft.dropdown.Option("M95"),
                ft.dropdown.Option("M88"),
            ],
            on_change=self.select_material,
        )


    def build(self):
        self.header = ft.Column(
            controls=[
                ft.Row(
                    alignment=ft.alignment.center,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10,
                    controls=[
                        #self.banner,
                        self.number,
                        self.material,
                        self.elongation_threshold,
                        self.stress_threshold,
                    ],
                ),
            ft.Divider(thickness=5, color=ft.colors.BLUE_GREY)
            ],
        )
        return self.header
    


    def change_build_number(self, e):
        print("current value in number field:")
        print(self.number.value)
        #self.banner.open = True
        self.update()
    '''
    def change_number(self, e):
        #self.banner.open = False
        # update previous number
        self.previous_number = self.number.value
        # write previous number to current number
        self.number.value = self.previous_number
        self.material.value = ''
        self.update()

    def ignore(self, e):
        #self.banner.open = False
        # set current number to previous 
        self.number.value = self.previous_number
        self.update()
    '''




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
        # self.file_picker =ft.FilePicker(on_result=self.process_file,visible=True)
        self.file_path =  ft.TextField(label='File',           value='', expand=3, read_only=True)
        self.number =     ft.TextField(label='Number',         value='', expand=1)
        self.length =     ft.TextField(label='Length [mm]',    value='', expand=2)
        self.width =      ft.TextField(label='Width [mm]',     value='', expand=2)
        self.thickness =  ft.TextField(label='Thickness [mm]', value='', expand=2)
        self.elongation = ft.TextField(label='Elongation [%]', value='', expand=2, read_only=True)
        self.stress =     ft.TextField(label='Stress [MPA]',   value='', expand=2, read_only=True)
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
                #self.file_picker,
                self.file_path, 
                self.number, 
                self.length, 
                self.width, 
                self.thickness, 
                self.elongation, 
                self.stress,
                self.lock,
                self.unlock,
                self.delete,
                ],
        )
        return self.view
    
    #########################################################################
    # data processing area

    def process_dog_bone(self, e, material, data_file_path):
        # load the data
        os.chmod(data_file_path, stat.S_IRWXO)
        # open the file
        report = open(data_file_path, 'r')
        # get the data out of the html
        data = parse_report(report)
        # REMEMBER the columns are : columns=['Reading Number', 'Load [N]', 'Travel [mm]', 'Time [sec]'])

        # calculate the values, results
        # score the results
        # write results to fields
        # write scores to colors
        # update dog bone
        self.elongation.bgcolor = value_to_color(material, "STRESS", 2.0)
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
    def __init__(self, x, y, w, h):
        super().__init__()
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        
    def build(self):
        
        self.message = ft.TextField(label="Message", value='', read_only=True, expand=2)
        self.header = Build()
        self.dog_bones = ft.Column()
        self.get_directory_dialog = ft.FilePicker(on_result=self.get_directory_result)
        
        # application's root control (i.e. "view") containing all other controls
        return ft.Column(
            spacing=10,
            width=1500,
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
                ft.Row(
                    controls=[
                        ft.FloatingActionButton(icon=ft.icons.CREATE, text="Create Build Report", expand=1, bgcolor=ft.colors.GREEN, on_click=self.save_build),
                        ft.FloatingActionButton(icon=ft.icons.FOLDER, text="Review Build Report",      expand=1, bgcolor=ft.colors.AMBER  , on_click=self.review_build),
                        self.get_directory_dialog,
                    ],
                ),
            ],
        )

    def add_clicked(self, e):
        new_dog_bone = DogBone(self.remove_dog_bone)
        new_dog_bone.number.value = str(len(self.dog_bones.controls)+1)
        self.dog_bones.controls.append(new_dog_bone)
        # this line will be important
        #self.dog_bones.controls[1].elongation.bgcolor=ft.colors.RED
        self.update()

    def remove_dog_bone(self, dog_bone):
        self.dog_bones.controls.remove(dog_bone)
        self.update()

    def save_build(self, e):
        # all of the dog bone unlocks need to be visible true in order to save a build
        if all([db.unlock.visible for db in self.dog_bones.controls]) == True:
            self.message.value = "* Build Report Saved *"
            self.message.bgcolor = ft.colors.GREEN_400
            self.update()
            self.capture_build(e)

        else:
            self.message.value = "Please Lock All Dog Bones"
            self.message.bgcolor = ft.colors.AMBER
            self.update()

    def capture_build(self, e):
        print("HERE")
        self.page.window_maximized = True
        self.page.update()
        time.sleep(0.5)
        screenshot = ImageGrab.grab()
        self.page.window_maximized = False
        self.page.update()

        filepath = os.path.join(self.build_directory, "Report"+str(time.time()).strip('.')[0]+'.png')
        print(filepath)
        screenshot.save(filepath, 'PNG')

    def review_build(self, e):
        self.message.value = "Report Loaded"
        self.message.bgcolor = ft.colors.GREEN_400
        print("review build")
        self.update()

    def get_directory_result(self, e: ft.FilePickerResultEvent):
        if len(self.dog_bones.controls) == 0:
            self.message.value = "Please Add Some Dog Bones Before Selecting Build"
            self.message.bgcolor = ft.colors.AMBER
            self.update()
        else:
            if all([db.unlock.visible for db in self.dog_bones.controls]) == True:
                try:
                    self.message.value = e.path if e.path else "Cancelled!"
                    build_files = os.listdir(self.message.value)
                    build_files = [f for f in build_files if f.endswith('.html')]
                    print(build_files)
                    # for every file in the folder, do stuff
                    for i in range(len(build_files)):
                        print(build_files[i])
                        self.dog_bones.controls[i].file_path.value = build_files[i]
                        self.build_directory = e.path
                        self.data_file_path = os.path.join(e.path, str(build_files[i]))
                        print(self.data_file_path)
                        self.dog_bones.controls[i].process_dog_bone(e, self.header.material.value, self.data_file_path)
                        self.dog_bones.controls[i].update()
                    self.message.bgcolor = ft.colors.WHITE
                    self.message.update()
                    self.update()

                except IndexError:
                    self.message.bgcolor = ft.colors.AMBER
                    self.message.value = "Different Number of Dog Bones vs Dog Bone Files"
                    self.update()
                except KeyError:
                    self.message.bgcolor = ft.colors.AMBER
                    self.message.value = "Make Sure to Select a Material"
                    self.update()
                
                except FileNotFoundError:
                    self.message.bgcolor = ft.colors.AMBER
                    self.message.value = "Looks Like There Was an Error Loading the Files. Try Again"
                    self.update()



            else:
                self.message.value = "Please Lock All Dog Bones Before Selecting Build"
                self.message.bgcolor = ft.colors.AMBER
                self.update()




def main(page: ft.Page):
    page.title = "Dog Bone App"
    page.scroll = ft.ScrollMode.ALWAYS
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.update()
    x = page.window_left
    y = page.window_top 
    w = page.window_max_width 
    h = page.window_max_height
    print(x,y,w,h)
    # create application instance
    dog_bone_app = DogBoneApp(x,y,w,h)

    # add application's root control to the page
    page.add(dog_bone_app)

ft.app(target=main)