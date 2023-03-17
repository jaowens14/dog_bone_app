import pandas as pd

lt = pd.read_csv('.\\lt3.csv').transpose()
print(lt)

header = lt.loc['Material_Statistic']
print("THis is the header", header)
lt = lt.drop('Material_Statistic')
for index, row in lt.iterrows():
    row = pd.concat([header, row], axis=1).transpose()
    val = row['M95_AVE']
    
    print(row)
#print(lt)
'''
lt = {
    'M95': {
    '1':{'L':{'AVE':75, 'STD':0.1}, 'W':{'AVE':4, 'STD':0.1}, 'H':{'AVE':2, 'STD':0.1}, 'F':{'AVE':50, 'STD':0.1}, 'E':{'AVE':20, 'STD':0.1}},
    '2':{'L':{'AVE':75, 'STD':0.1}, 'W':{'AVE':4, 'STD':0.1}, 'H':{'AVE':2, 'STD':0.1}, 'F':{'AVE':50, 'STD':0.1}, 'E':{'AVE':20, 'STD':0.1}},
    '3':{'L':{'AVE':75, 'STD':0.1}, 'W':{'AVE':4, 'STD':0.1}, 'H':{'AVE':2, 'STD':0.1}, 'F':{'AVE':50, 'STD':0.1}, 'E':{'AVE':20, 'STD':0.1}},
    '4':{'L':{'AVE':75, 'STD':0.1}, 'W':{'AVE':4, 'STD':0.1}, 'H':{'AVE':2, 'STD':0.1}, 'F':{'AVE':50, 'STD':0.1}, 'E':{'AVE':20, 'STD':0.1}},
    '5':{'L':{'AVE':75, 'STD':0.1}, 'W':{'AVE':4, 'STD':0.1}, 'H':{'AVE':2, 'STD':0.1}, 'F':{'AVE':50, 'STD':0.1}, 'E':{'AVE':20, 'STD':0.1}},
    '6':{'L':{'AVE':75, 'STD':0.1}, 'W':{'AVE':4, 'STD':0.1}, 'H':{'AVE':2, 'STD':0.1}, 'F':{'AVE':50, 'STD':0.1}, 'E':{'AVE':20, 'STD':0.1}},
    '7':{'L':{'AVE':75, 'STD':0.1}, 'W':{'AVE':4, 'STD':0.1}, 'H':{'AVE':2, 'STD':0.1}, 'F':{'AVE':50, 'STD':0.1}, 'E':{'AVE':20, 'STD':0.1}},
    '8':{'L':{'AVE':75, 'STD':0.1}, 'W':{'AVE':4, 'STD':0.1}, 'H':{'AVE':2, 'STD':0.1}, 'F':{'AVE':50, 'STD':0.1}, 'E':{'AVE':20, 'STD':0.1}},
    '9':{'L':{'AVE':75, 'STD':0.1}, 'W':{'AVE':4, 'STD':0.1}, 'H':{'AVE':2, 'STD':0.1}, 'F':{'AVE':50, 'STD':0.1}, 'E':{'AVE':20, 'STD':0.1}},
    },
    'M88': {
    '1':{'L':{'AVE':75, 'STD':0.1}, 'W':{'AVE':4, 'STD':0.1}, 'H':{'AVE':2, 'STD':0.1}, 'F':{'AVE':50, 'STD':0.1}, 'E':{'AVE':20, 'STD':0.1}},
    '2':{'L':{'AVE':75, 'STD':0.1}, 'W':{'AVE':4, 'STD':0.1}, 'H':{'AVE':2, 'STD':0.1}, 'F':{'AVE':50, 'STD':0.1}, 'E':{'AVE':20, 'STD':0.1}},
    '3':{'L':{'AVE':75, 'STD':0.1}, 'W':{'AVE':4, 'STD':0.1}, 'H':{'AVE':2, 'STD':0.1}, 'F':{'AVE':50, 'STD':0.1}, 'E':{'AVE':20, 'STD':0.1}},
    '4':{'L':{'AVE':75, 'STD':0.1}, 'W':{'AVE':4, 'STD':0.1}, 'H':{'AVE':2, 'STD':0.1}, 'F':{'AVE':50, 'STD':0.1}, 'E':{'AVE':20, 'STD':0.1}},
    '5':{'L':{'AVE':75, 'STD':0.1}, 'W':{'AVE':4, 'STD':0.1}, 'H':{'AVE':2, 'STD':0.1}, 'F':{'AVE':50, 'STD':0.1}, 'E':{'AVE':20, 'STD':0.1}},
    '6':{'L':{'AVE':75, 'STD':0.1}, 'W':{'AVE':4, 'STD':0.1}, 'H':{'AVE':2, 'STD':0.1}, 'F':{'AVE':50, 'STD':0.1}, 'E':{'AVE':20, 'STD':0.1}},
    '7':{'L':{'AVE':75, 'STD':0.1}, 'W':{'AVE':4, 'STD':0.1}, 'H':{'AVE':2, 'STD':0.1}, 'F':{'AVE':50, 'STD':0.1}, 'E':{'AVE':20, 'STD':0.1}},
    '8':{'L':{'AVE':75, 'STD':0.1}, 'W':{'AVE':4, 'STD':0.1}, 'H':{'AVE':2, 'STD':0.1}, 'F':{'AVE':50, 'STD':0.1}, 'E':{'AVE':20, 'STD':0.1}},
    '9':{'L':{'AVE':75, 'STD':0.1}, 'W':{'AVE':4, 'STD':0.1}, 'H':{'AVE':2, 'STD':0.1}, 'F':{'AVE':50, 'STD':0.1}, 'E':{'AVE':20, 'STD':0.1}},
    },
    'PA12': {
    '1':{'L':{'AVE':75, 'STD':0.1}, 'W':{'AVE':4, 'STD':0.1}, 'H':{'AVE':2, 'STD':0.1}, 'F':{'AVE':50, 'STD':0.1}, 'E':{'AVE':20, 'STD':0.1}},
    '2':{'L':{'AVE':75, 'STD':0.1}, 'W':{'AVE':4, 'STD':0.1}, 'H':{'AVE':2, 'STD':0.1}, 'F':{'AVE':50, 'STD':0.1}, 'E':{'AVE':20, 'STD':0.1}},
    '3':{'L':{'AVE':75, 'STD':0.1}, 'W':{'AVE':4, 'STD':0.1}, 'H':{'AVE':2, 'STD':0.1}, 'F':{'AVE':50, 'STD':0.1}, 'E':{'AVE':20, 'STD':0.1}},
    '4':{'L':{'AVE':75, 'STD':0.1}, 'W':{'AVE':4, 'STD':0.1}, 'H':{'AVE':2, 'STD':0.1}, 'F':{'AVE':50, 'STD':0.1}, 'E':{'AVE':20, 'STD':0.1}},
    '5':{'L':{'AVE':75, 'STD':0.1}, 'W':{'AVE':4, 'STD':0.1}, 'H':{'AVE':2, 'STD':0.1}, 'F':{'AVE':50, 'STD':0.1}, 'E':{'AVE':20, 'STD':0.1}},
    '6':{'L':{'AVE':75, 'STD':0.1}, 'W':{'AVE':4, 'STD':0.1}, 'H':{'AVE':2, 'STD':0.1}, 'F':{'AVE':50, 'STD':0.1}, 'E':{'AVE':20, 'STD':0.1}},
    '7':{'L':{'AVE':75, 'STD':0.1}, 'W':{'AVE':4, 'STD':0.1}, 'H':{'AVE':2, 'STD':0.1}, 'F':{'AVE':50, 'STD':0.1}, 'E':{'AVE':20, 'STD':0.1}},
    '8':{'L':{'AVE':75, 'STD':0.1}, 'W':{'AVE':4, 'STD':0.1}, 'H':{'AVE':2, 'STD':0.1}, 'F':{'AVE':50, 'STD':0.1}, 'E':{'AVE':20, 'STD':0.1}},
    '9':{'L':{'AVE':75, 'STD':0.1}, 'W':{'AVE':4, 'STD':0.1}, 'H':{'AVE':2, 'STD':0.1}, 'F':{'AVE':50, 'STD':0.1}, 'E':{'AVE':20, 'STD':0.1}},
    },
    'PA11': {
    '1':{'L':{'AVE':75, 'STD':0.1}, 'W':{'AVE':4, 'STD':0.1}, 'H':{'AVE':2, 'STD':0.1}, 'F':{'AVE':50, 'STD':0.1}, 'E':{'AVE':20, 'STD':0.1}},
    '2':{'L':{'AVE':75, 'STD':0.1}, 'W':{'AVE':4, 'STD':0.1}, 'H':{'AVE':2, 'STD':0.1}, 'F':{'AVE':50, 'STD':0.1}, 'E':{'AVE':20, 'STD':0.1}},
    '3':{'L':{'AVE':75, 'STD':0.1}, 'W':{'AVE':4, 'STD':0.1}, 'H':{'AVE':2, 'STD':0.1}, 'F':{'AVE':50, 'STD':0.1}, 'E':{'AVE':20, 'STD':0.1}},
    '4':{'L':{'AVE':75, 'STD':0.1}, 'W':{'AVE':4, 'STD':0.1}, 'H':{'AVE':2, 'STD':0.1}, 'F':{'AVE':50, 'STD':0.1}, 'E':{'AVE':20, 'STD':0.1}},
    '5':{'L':{'AVE':75, 'STD':0.1}, 'W':{'AVE':4, 'STD':0.1}, 'H':{'AVE':2, 'STD':0.1}, 'F':{'AVE':50, 'STD':0.1}, 'E':{'AVE':20, 'STD':0.1}},
    '6':{'L':{'AVE':75, 'STD':0.1}, 'W':{'AVE':4, 'STD':0.1}, 'H':{'AVE':2, 'STD':0.1}, 'F':{'AVE':50, 'STD':0.1}, 'E':{'AVE':20, 'STD':0.1}},
    '7':{'L':{'AVE':75, 'STD':0.1}, 'W':{'AVE':4, 'STD':0.1}, 'H':{'AVE':2, 'STD':0.1}, 'F':{'AVE':50, 'STD':0.1}, 'E':{'AVE':20, 'STD':0.1}},
    '8':{'L':{'AVE':75, 'STD':0.1}, 'W':{'AVE':4, 'STD':0.1}, 'H':{'AVE':2, 'STD':0.1}, 'F':{'AVE':50, 'STD':0.1}, 'E':{'AVE':20, 'STD':0.1}},
    '9':{'L':{'AVE':75, 'STD':0.1}, 'W':{'AVE':4, 'STD':0.1}, 'H':{'AVE':2, 'STD':0.1}, 'F':{'AVE':50, 'STD':0.1}, 'E':{'AVE':20, 'STD':0.1}},
    },
}

print(lt['M88']['1']['L']['AVE'])

for mat in lt:
    for num in lt[mat]:
        for prop in lt[mat][num]:
            for stat in lt[mat][num][prop]:

                lt[mat][num][prop][stat] = 1
'''

                