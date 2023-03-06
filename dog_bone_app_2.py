import flet as ft


class Header(ft.UserControl):
    def __init__(self):
        super().__init__()
        
    def build(self):
        self.header = 





class DogBoneApp(ft.UserControl):
    def build(self):
        self.header = ft.TextField(hint_text="Header")
        self.dogbones = ft.Column()

        return ft.Column(
            width=600,
            controls=[
                ft.Row(
                    controls=[
                        self.header,
                        ft.FloatingActionButton(icon=ft.icons.ADD, on_click=self.add_dog_bone)
                    ],
                ),
                self.dogbones,
            ],
        )
    
    def add_dog_bone(self, e):
        #self.dogbones.controls.append(ft.)