# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 13:50:18 2019

@author: sriniwas
"""

import csv
import pandas as pd
import numpy as np 
from plagiarism import plag_calc

def generate_csv(parentID, solutions, weights):
    print("Evaluating results...")
    answers = []
    sol = []
    marks = []
    data = pd.read_csv(solutions)
    answers = data['Solution'].tolist()
    marks = data['Marks'].tolist()
    data.columns = range(data.shape[1])
    data = data.drop(data.columns[0], axis=1)
    for i in answers:
        j = str(i)
        if i is np.nan:
            sol.append("")
        elif j.find("~!")!=-1:
            sol.append(sorted(j.split("~!")))
            sol[-1] = [st.lower() for st in sol[-1]]
            for ipp in range(0,len(sol[-1])):
                sol[-1][ipp] = sol[-1][ipp].replace("+", "-")
        else:
            sol.append(j)
    #print(data)
    wht = []
    with open(weights, 'r') as f:
      reader = csv.reader(f)
      wht = list(reader)
    #new_matrix = wht / row_sums[:, numpy.newaxis]
    #ans = plag_calc(parentID,sol,marks,weights)
    wht = wht[1:][0]
    s = sum(float(i) for i in wht)
    for i in range(len(wht)):
        wht[i] = float(wht[i])/s
    ans = plag_calc(parentID,sol,marks,wht)
    plag = np.asarray(ans)
    plag = plag[plag[:,-1].argsort()][::-1]
    print("Saving results to plagarism.csv")
    np.savetxt('plagarism.csv', plag, delimiter=',', fmt='%s')
    print("Success!")
    

generate_csv(3,"solutions.csv", "weights.csv")
