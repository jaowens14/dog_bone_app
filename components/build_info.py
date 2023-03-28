import flet as ft


BUILD_MATERIALS = ["PA12", "PA11", "M95", "M88"]

MATERIAL_THRESHOLDS = {
    'M95' :  {
        "STRESS" : {
            "STD":3.0, 
            "AVE": 20.0
        }, 
        "ELONGATION" : {
            "STD":3.0, 
            "AVE":20.0
        }
    },
    'M88' :  {
        "STRESS" : {
            "STD":3.0, 
            "AVE": 20.0
        }, 
        "ELONGATION" : {
            "STD":3.0, 
            "AVE":20.0
        }
    },
    'PA12' : {
        "STRESS" : {
            "STD":3.0, 
            "AVE": 20.0
        }, 
        "ELONGATION" : {
            "STD":3.0, 
            "AVE":20.0
        }
    },
    'PA11' : {
        "STRESS" : {
            "STD":3.0, 
            "AVE": 20.0
        }, 
        "ELONGATION" : {
            "STD":3.0, 
            "AVE":20.0
        }
    },
}


class BuildInfo(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.previous_number = '0000'
        self.number = self.get_number()
        self.elongation_threshold = self.get_elongation_threshold()
        self.stress_threshold = self.get_stress_threshold()
        self.material = self.get_material()

    def change_build_number(self, e):
        print(self.number.value)
        self.update()

    def get_number(self):
        return ft.TextField(
            label='Build Number',
            value='0000', 
            expand=4, 
            on_blur=self.change_build_number
        )

    def get_elongation_threshold(self):
        return ft.TextField(
            label='Elongation Threshold', 
            value='', 
            expand=2, 
            read_only=True
        )

    def get_stress_threshold(self):
        return ft.TextField(
            label='Stress Threshold',
            value='', 
            expand=2, 
            read_only=True
        )

    def select_material(self, e):
        self.stress_threshold.value  = MATERIAL_THRESHOLDS[self.material.value]['STRESS']['AVE']
        self.elongation_threshold.value = MATERIAL_THRESHOLDS[self.material.value]['ELONGATION']['AVE']
        self.update()

    def get_material(self):
        return ft.Dropdown(
            label="Build Material",
            options=[ft.dropdown.Option(material) for material in BUILD_MATERIALS],
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

    

    