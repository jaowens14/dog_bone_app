import pandas as pd
import numpy as np
import flet as ft
from lookup_table import lookup
#  |red------ -2 std---yellow-- -std      average     +std    +2 std


def grade_dog_bone(material, dog_bone_number, length, width, thickness, percent_elongation, force):    
    averages = lookup(material, 'AVE', dog_bone_number)
    stds     = lookup(material, 'STD', dog_bone_number)
    sample = {'Length': length, 'Width': width, 'Thickness': thickness, 'Force': force, 'Elongation': percent_elongation}
    output = {}
    for k,v in sample.items():
        output[k] = color_map(float(v), float(averages[k]), float(stds[k]), float(2*stds[k]))
    return output

def color_map(value, ave, std, std2):
    print(value)

    if value <= ave+2*std and value >= ave-2*std:
        print("value within 1 STD set to green")
        color = ft.colors.GREEN_300

    elif value <= ave+2*std2 and value >= ave-2*std2:
        print("Value within 2 STD set to yellow")
        color = ft.colors.AMBER_300

    elif value >= ave+2*std2 or value <= ave-2*std2:
        print("value is below 2 std or above 2 std, set to red")
        color = ft.colors.RED_300
    else:
        print("error in color map")
        color = ft.colors.PURPLE_300
    return color



#grade_dog_bone("M95", "1", "75", "4", "2", "20", "20")   
