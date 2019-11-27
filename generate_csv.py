##@file plagiarism.py
#@brief This file of the project takes input of files from user and converts those files to array of list formats so as to take in
#use aftterwards.
#@details This is 
#@author Infernos : CS699 Course Project Software Lab
#@date Thursday, November 29, 2019

##Include section
import csv
import pandas as pd
import numpy as np 
import argparse
from plagiarism import plag_calc

##
#@brief This function takes testID, solutions csv path and weights csv path as an arguments and generating the output plagarism index in a csv file.
#@details In this the solutions csv file is first structured in a formt so the other functions can compare the answers given by students
#with correct answer efficiently. Also the weights are being extracted from its location and normalized in this function. Finally all these
#are passed to another function that is checking plagarism and returning a numpy array having the plagarism index.
#@param parentID int 
#@param solutions str 
#@param weights str
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Say hello')
    parser.add_argument("-i", "--testID", help="Test ID")
    parser.add_argument("-s", "--solutions", help="Path of solutions csv file")
    parser.add_argument("-w", "--weights", help="Path of weights csv file")
    args = parser.parse_args()
    
    generate_csv(args.testID, args.solutions, args.weights)