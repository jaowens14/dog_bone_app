import flet as ft

class DogBone(ft.UserControl):
    def __init__(self, file_path, number, length, width, thickness):
        super().__init__()
        self.file_path = file_path
        self.number    = number
        self.length    = length
        self.width     = width
        self.thickness = thickness


    def build(self):

        self.dog_bone = ft.Row(
            spacing=1,
            controls=[
                ft.TextField(value=self.file_path)
            ]
        )



        return self.dog_bone
    

class DogBoneApp(ft.UserControl):
    def build(self):
        self.test = ft.TextField(hint_text="Enter a number")
        self.add_dog_bone_button = ft.IconButton
        return ft.Column(
                width=600,
                controls=[
                    self.test
                ]
        )


def main(page: ft.Page):
    page.title = "DOG BONE APP"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.update()

    dog_bone_app = DogBoneApp()
    dog_bone = DogBone('test', 3,0.0,0.1,0.2)
    page.add(dog_bone)
    page.add(dog_bone_app)

ft.app(target=main)