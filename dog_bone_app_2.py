import flet as ft


class Build(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.number =               ft.TextField(label='Build Number',         value='', expand=2)
        self.elongation_threshold = ft.TextField(label='Elongation Threshold', value='', expand=1, read_only=True)
        self.stress_threshold =     ft.TextField(label='Stress Threshold',     value='', expand=1, read_only=True)

        self.material = ft.Dropdown(
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

    def select_material(self, e):
        material_thresholds = {
        'M95' :  {"ENGINEERING STRESS" : 5.1, "PERCENT ELONGATION" : 15},
        'M88' :  {"ENGINEERING STRESS" : 6.2, "PERCENT ELONGATION" : 15},
        'PA12' : {"ENGINEERING STRESS" : 7.3, "PERCENT ELONGATION" : 15},
        'PA11' : {"ENGINEERING STRESS" : 8.4, "PERCENT ELONGATION" : 15},
        }

        self.stress_threshold.value  = material_thresholds[self.material.value]['ENGINEERING STRESS']
        self.elongation_threshold.value = material_thresholds[self.material.value]['PERCENT ELONGATION']

        self.update()
        


    

class DogBone(ft.UserControl):
    def __init__(self, delete_func):
        super().__init__()
        # self.file_picker =ft.FilePicker(on_result=self.process_file,visible=True)
        self.file_path =  ft.TextField(label='File',           value='', expand=1)
        self.number =     ft.TextField(label='Dog Bone Number',value='', expand=2)
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
        self.update()

    def unlock_dog_bone(self, e):
        self.unlock.visible = False
        self.lock.visible = True
        self.file_path.read_only = False
        self.number.read_only    = False
        self.length.read_only    = False
        self.width.read_only     = False
        self.thickness.read_only = False
        self.update()

    def process_file(self, e):
        print("processed file")



class DogBoneApp(ft.UserControl):
    def build(self):
        self.header = Build()
        self.dog_bones = ft.Column()

        # application's root control (i.e. "view") containing all other controls
        return ft.Column(
            spacing=10,
            width=1500,
            controls=[
                self.header,
                ft.Row(
                    controls=[
                        ft.FloatingActionButton(icon=ft.icons.ADD, on_click=self.add_clicked, text="Add A Dog Bone", expand=1),
                        ft.TextField(label="Error Messages", value='', read_only=True, expand=2),
                    ],
                ),
                self.dog_bones,
                ft.Divider(thickness=5, color=ft.colors.BLUE_GREY),
                ft.Row(
                    controls=[
                        ft.FloatingActionButton(icon=ft.icons.CREATE, text="Create Build Report", expand=1, bgcolor=ft.colors.GREEN),
                        ft.FloatingActionButton(icon=ft.icons.DELETE, text="Clear All Data", expand=1, bgcolor=ft.colors.RED)
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


def main(page: ft.Page):
    page.title = "Dog Bone App"
    page.scroll = ft.ScrollMode.ALWAYS
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.update()

    # create application instance
    dog_bone_app = DogBoneApp()

    # add application's root control to the page
    page.add(dog_bone_app)

ft.app(target=main)