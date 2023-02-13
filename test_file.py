thresholds = {
    'm95' : {"tensile_strength" : 75, "elongation_%" : 151},
    'm88' : {"tensile_strength" : 76, "elongation_%" : 152},
    'pa12' : {"tensile_strength" : 77, "elongation_%" : 153},
    'pa11' : {"tensile_strength" : 78, "elongation_%" : 154},
}

print(thresholds)
print(thresholds["m88"]['tensile_strength'])

header = list({'BUILD NUMBER': '00000', 'MATERIAL': 'PA12', 'DOG BONE NUMBER': '5', 'LENGTH': '75.00', 'WIDTH': '4.0', 'THICKNESS': '2.0'})

