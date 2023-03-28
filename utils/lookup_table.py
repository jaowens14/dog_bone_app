import pandas as pd
from os import path

def lookup(material, statistic, dog_bone_number):
    dog_bone_number = int(dog_bone_number)
    lt_path = path.abspath(path.join(path.dirname(__file__), 'assets','lt5.csv'))
    lt = pd.read_csv(lt_path)
    props = lt.loc[(lt['Material'] == material) & (lt['Statistic'] ==statistic) & (lt['Dog Bone Number'] == dog_bone_number)]

    mat =  props.iloc[0]["Material"]
    stat = props.iloc[0]["Statistic"]
    num =  props.iloc[0]["Dog Bone Number"]
    L =    props.iloc[0]["L"]
    W =    props.iloc[0]["W"]
    T =    props.iloc[0]["H"]
    F =    props.iloc[0]["F"]
    E =    props.iloc[0]["E"]
    data = {
        "Length": L,
        "Width": W,
        "Thickness": T,
        "Force": F,
        "Elongation":E,
        }
    # {'Material': 'M95', 'Statistic': 'AVE', 'Dog Bone Number': 4, 'Length': 75.45857143, 'Width': 4.218571429, 'Thickness': 2.153571429, 'Force': 68.46428571, 'Elongation': 17.38857143}
    return data
