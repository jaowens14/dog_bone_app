import flet as ft
import time 
import os
import stat
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pandas as pd
import numpy as np
from parse_html import parse_report
import matplotlib.pyplot as plt

thresholds = {
    'm95' : {"tensile_strength" : 75, "elongation_%" : 151},
    'm88' : {"tensile_strength" : 76, "elongation_%" : 152},
    'pa12' : {"tensile_strength" : 77, "elongation_%" : 153},
    'pa11' : {"tensile_strength" : 78, "elongation_%" : 154},
}

print(thresholds)
print(thresholds["m88"]['tensile_strength'])

header = list({'BUILD NUMBER': '00000', 'MATERIAL': 'PA12', 'DOG BONE NUMBER': '5', 'LENGTH': '75.00', 'WIDTH': '4.0', 'THICKNESS': '2.0'})

# open the file
report = open('.\\02092023-01.html', 'r')

# parse the file
sample_header, sample_data = parse_report(report)

print(sample_header)
print(sample_header['BUILD NUMBER'])
# {'BUILD NUMBER': '00000', 'MATERIAL': 'PA12', 'DOG BONE NUMBER': '5', 'LENGTH': '75.00', 'WIDTH': '4.0', 'THICKNESS': '2.0'}

max_travel = sample_data
sample_data['Load [N]'] = -sample_data['Load [N]'].astype(float)
sample_data['Travel [mm]'] = sample_data['Travel [mm]'].astype(float)
max_load = sample_data['Load [N]'].max()
elongation_at_max_load = sample_data.loc[sample_data["Load [N]"] == max_load, 'Travel [mm]']

print(elongation_at_max_load)
cross_section_area = float(sample_header['THICKNESS'])*float(sample_header['WIDTH'])

print('area', cross_section_area)
plt.plot(sample_data['Load [N]'])
plt.plot(sample_data['Travel [mm]'])
plt.show()

print(sample_data["Load [N]"])
print(sample_data['Load [N]'].min())
print(sample_data['Travel [mm]'].max())