##@file plagiarism.py
#@brief This file of the project extracts strored data of responses from the database and evaluates a normalised plagiarism index.
#@details This is the python script which will automatically check for plagiarism. For each roll number all it's answers to the test 
#questions are extracted from the database. Then for each question's answer, his response is checked pairwise with all the other
#responses submitted for the same test. Plagiarism indices corresponding to each answer with each other student's response are stored
#in output csv. And finally weighted plagiarism index according to the distribution of marks of the questions is evaluated and returned.
#@author Infernos : CS699 Course Project Software Lab
#@date Thursday, November 29, 2019

##Include section
import csv
import pandas as pd
import numpy as np 
from plagiarism import plag_calc
##
#@brief This function is taking a filename as argument and returning a list of integers inside the file.
#@details The given file contains integers each line. This function is picking out text line by line, typecasting it to integers
#and appending it to a list. Finally it is returning that list.
#@return l list 
#@param filename the name of the file 
#
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
