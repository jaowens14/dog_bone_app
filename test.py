import pandas as pd
import numpy as np

test_data = pd.read_csv("test_file.csv").to_numpy()

s = np.max(test_data[:,0])
p = np.max(test_data[:,1])
print(s,p)


