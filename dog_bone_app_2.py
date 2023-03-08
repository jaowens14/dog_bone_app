import flet as ft

class DogBone(ft.UserControl):
    def __init__(self, file_path, number, length, width, thickness, delete):
        super().__init__()
        self.file_path = file_path
        self.number    = number
        self.length    = length
        self.width     = width
        self.thickness = thickness
        self.delete = delete


    def build(self):

        self.dog_bone = ft.Row(
            spacing=1,
            controls=[
                ft.TextField(hint_text="File goes here"),
                ft.TextField(hint_text="dog bone number here"),
                ft.IconButton(icon=ft.icons.DELETE, on_click=self.remove_dog_bone)
            ]
        )

        return self.dog_bone
    
    def remove_dog_bone(self, e):
        self.

    

class DogBoneApp(ft.UserControl):
    def build(self):
        self.test = ft.TextField(hint_text="Enter a number")
        self.add_dog_bone_button = ft.IconButton(icon=ft.icons.ADD, on_click=self.add_dog_bone,)
        #self.submit_button = ft.IconButton(icon=ft.icons.CHECK, on_click=self.submit_build)
        self.dog_bones = ft.Column()
        return ft.Column(
                width=600,
                controls=[
                    self.test,
                    self.add_dog_bone_button,
                    self.dog_bones,
                ]
        )
    def add_dog_bone(self, e):
        self.dog_bone = DogBone('',1,2,3,4)
        self.dog_bones.controls.append(self.dog_bone)
        print("add dog bone button pressed")
        self.update()
    
    def remove_dog_bone(self, dog_bone):
        self.dog_bones.controls.remove(dog_bone)
        self.update()



def main(page: ft.Page):
    page.title = "DOG BONE APP"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.update()

    dog_bone_app = DogBoneApp()
    page.add(dog_bone_app)

ft.app(target=main)