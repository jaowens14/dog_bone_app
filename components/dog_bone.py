import sys

sys.path.insert(0, '../')

from flet import (
    UserControl, 
    TextButton, 
    TextField, 
    IconButton, 
    icons, 
    colors, 
    Row, 
    alignment, 
    CrossAxisAlignment
)

from utils.color_map import grade_dog_bone


class DogBone(UserControl):
    def __init__(self, delete_func):
        super().__init__()
        self.delete_func = delete_func
        self.entry_number = TextButton(text='', expand=2)
        self.number = self.get_text_field(label='File', expand=30, read_only=True)
        self.number = self.get_text_field(label='Number', expand=15)
        self.length = self.get_text_field(label='Length [mm]', expand=25)
        self.width = self.get_text_field(label='Width [mm]', expand=25)
        self.thickness = self.get_text_field(label='Thickness [mm]', expand=25)
        self.elongation = self.get_text_field(label='Elongation [%]', expand=25, read_only=True)
        self.force = self.get_text_field(label='Force [N]', expand=25, read_only=True)
        self.stress = self.get_text_field(label='Stress [MPA]', expand=25, read_only=True)
        self.delete = self.get_icon_button(icons.DELETE, on_click=self.delete_dog_bone)
        self.lock = self.get_icon_button(icons.LOCK_OPEN_OUTLINED, on_click=self.lock_dog_bone)
        self.locunlockk = self.get_icon_button(icons.LOCK_OUTLINED, on_click=self.unlock_dog_bone, visible=False)

    def get_text_field(self, label, expand, bgcolor=colors.BLUE_GREY_50, value='', read_only=False):
        return TextField(label=label, value=value, expand=expand, bgcolor=bgcolor, read_only=read_only)

    def get_icon_button(self, icon, on_click, visible=True):
        return IconButton(icon, on_click=on_click, visible=visible)

    def build(self):
        return Row(
            alignment=alignment.center,
            vertical_alignment=CrossAxisAlignment.CENTER,
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

    def process_dog_bone(self, e, dog_bone_number, material, data_file_path):
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
        self.force.value = sample_data['Load [N]'].max()
        travel_at_max_load = max(sample_data.loc[sample_data["Load [N]"] == self.force.value, 'Travel [mm]'])
        percent_elongation = round(((travel_at_max_load/25) * 100),2)

        #engineering_stress = round(max_load/cross_sectional_area, 4)

        self.elongation.value = percent_elongation
        # calculate the values, results, score the results, write results to fields, write scores to colors, pdate dog bone
        colors = grade_dog_bone(material, dog_bone_number, self.length.value, self.width.value, self.thickness.value, percent_elongation, self.force.value)
        print(colors)
        self.length.bgcolor = colors['Length']
        self.width.bgcolor = colors['Width']
        self.thickness.bgcolor = colors['Thickness']
        self.force.bgcolor = colors['Force']
        self.elongation.bgcolor = colors['Elongation']
        print(colors)

        self.update()
            
        print("processed dog bones")

    def delete_dog_bone(self, e):
        self.delete_func(self)

    def lock_dog_bone(self, e):
        self.lock.visible = False
        self.unlock.visible = True
        self.file_path.read_only = True
        self.number.read_only = True
        self.length.read_only = True
        self.width.read_only = True
        self.thickness.read_only = True
        self.delete.visible = False
        self.update()

    def unlock_dog_bone(self, e):
        self.unlock.visible = False
        self.lock.visible = True
        self.file_path.read_only = True
        self.number.read_only = False
        self.length.read_only = False
        self.width.read_only = False
        self.thickness.read_only = False
        self.delete.visible = True
        self.update()