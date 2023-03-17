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
    print(ave)
    print(std)
    print(std2)
    if value > ave:
        print("value is at or above average, set to green")
        color = ft.colors.GREEN
    elif std < value < ave:
        print("Value is below average but above 1 std, set to yellow")
        color = ft.colors.AMBER
    elif std2 < value < std:
        print("value is below 1 std but above 2 std, set to red")
        color = ft.colors.RED
    elif value < std2:
        print("value is below 2 std, send warning or dark red?")
        color = ft.colors.DEEP_PURPLE
    else:
        print("error in color map")
    return color




