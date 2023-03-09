import pandas as pd
import numpy as np
import flet as ft

#  |red------ -2 std---yellow-- -std      average     +std    +2 std



material_thresholds = {
    'M95' :  {"STRESS" : {"STD":3.0, "AVE": 20.0}, "ELONGATION" : {"STD":3.0, "AVE":20.0}},
    'M88' :  {"STRESS" : {"STD":3.0, "AVE": 20.0}, "ELONGATION" : {"STD":3.0, "AVE":20.0}},
    'PA12' : {"STRESS" : {"STD":3.0, "AVE": 20.0}, "ELONGATION" : {"STD":3.0, "AVE":20.0}},
    'PA11' : {"STRESS" : {"STD":3.0, "AVE": 20.0}, "ELONGATION" : {"STD":3.0, "AVE":20.0}},
    }


def value_to_color(material, property, value):
    #print(material_thresholds["M88"]["STRESS"]["STD"])
    ave = material_thresholds[material][property]["AVE"]
    std = ave - material_thresholds[material][property]["STD"]
    std2 = std - material_thresholds[material][property]["STD"]

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




