import flet as ft


class Build(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.number = ft.TextField(label='Build Number', value='', expand=2)
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
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=50,
                    controls=[
                        self.number,
                        self.material,
                    ],
                ),
            ft.Divider(thickness=5)
            ],
        )
        
    
        return self.header
    
    
    def select_material(self, e):
        print('test')

        


    

class DogBone(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.file_path =  ft.TextField(label='File',value='', expand=2)
        self.number =     ft.TextField(label='Dog Bone Number',value='', expand=1)
        self.length =     ft.TextField(label='Length [mm]',value='', expand=1)
        self.width =      ft.TextField(label='Width [mm]',value='', expand=1)
        self.thickness =  ft.TextField(label='Thickness [mm]',value='', expand=1)
        self.elongation = ft.TextField(label='Elongation [%]',value='', expand=1)
        self.stress =     ft.TextField(label='Stress [MPA]',value='', expand=1)

    def build(self):

        self.view = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
            controls=[
                self.file_path, 
                self.number, 
                self.length, 
                self.width, 
                self.thickness, 
                self.elongation, 
                self.stress,
                ],
        )

        return self.view



class DogBoneApp(ft.UserControl):
    def build(self):
        self.title = ft.Text("TITLE")
        self.header = Build()
        self.dog_bones = ft.Column()

        # application's root control (i.e. "view") containing all other controls
        return ft.Column(
            spacing=60,
            width=600,
            controls=[
                self.header,
                ft.Row(
                    controls=[
                        self.title,
                        ft.FloatingActionButton(icon=ft.icons.ADD, on_click=self.add_clicked),
                    ],
                ),
                self.dog_bones,
            ],
        )

    def add_clicked(self, e):
        new_dog_bone = DogBone()
        new_dog_bone.number.value = str(len(self.dog_bones.controls)+1)
        self.dog_bones.controls.append(new_dog_bone)
        self.update()


def main(page: ft.Page):
    page.title = "ToDo App"
    page.scroll = ft.ScrollMode.ALWAYS
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.update()

    # create application instance
    dog_bone_app = DogBoneApp()

    # add application's root control to the page
    page.add(dog_bone_app)

ft.app(target=main)