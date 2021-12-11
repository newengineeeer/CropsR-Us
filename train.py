import pandas as pd
import numpy as np
from sklearn import linear_model
import pickle

df = pd.read_csv('dataset.csv')
reg = linear_model.LinearRegression()
reg.fit(df.drop('Yield',axis='columns'),df.Yield)
print(reg.coef_)
print(reg.intercept_)
filename = 'finalized_model.sav'
pickle.dump(reg, open(filename, 'wb'))
