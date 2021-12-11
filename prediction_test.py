import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn import metrics 
import pickle
import csv



with open('test_data.csv') as csv_file:
    csv_reader = csv.reader(csv_file)
    rows = list(csv_reader)
x=rows[98][:11]
x_actual=[]
for i in x:
    i=float(i)
    x_actual.append(i)

filename = "finalized_model.sav"
loaded_model = pickle.load(open(filename, 'rb'))
prediction=loaded_model.predict([x_actual])
print("row 99 of database= ", rows[98])
print("prediction= ",prediction[0])
print("true value= ",rows[98][11])


