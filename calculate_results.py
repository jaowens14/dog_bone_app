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


def calculate_results(material, property, value):

            cross_section_area = float(sample_header['THICKNESS'])*float(sample_header['WIDTH'])
            sample_data['Load [N]'] = -sample_data['Load [N]'].astype(float)
            sample_data['Travel [mm]'] = sample_data['Travel [mm]'].astype(float)
            max_load = sample_data['Load [N]'].max()
            travel_at_max_load = max(sample_data.loc[sample_data["Load [N]"] == max_load, 'Travel [mm]'])
            percent_elongation = round(((travel_at_max_load/25) * 100),2)
            engineering_stress = round(max_load/cross_section_area, 4)
    return color




