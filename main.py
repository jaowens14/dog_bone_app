import flet as ft
from components.dog_bone_app import DogBoneApp

def main(page: ft.Page):
    page.title = "Dog Bone App"
    page.scroll = ft.ScrollMode.ALWAYS
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.update()
    dog_bone_app = DogBoneApp()
    page.add(dog_bone_app)

if __name__ == "__main__":
    ft.app(target=main,assets_dir="assets")