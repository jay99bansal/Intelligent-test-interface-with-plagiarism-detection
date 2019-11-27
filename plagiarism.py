##@file plagiarism.py
#@brief This file of the project extracts strored data of responses from the database and evaluates a normalised plagiarism index.
#@details This is the python script which will automatically check for plagiarism. For each roll number all it's answers to the test 
#questions are extracted from the database. Then for each question's answer, his response is checked pairwise with all the other
#responses submitted for the same test. Plagiarism indices corresponding to each answer with each other student's response are stored
#in output csv. And finally weighted plagiarism index according to the distribution of marks of the questions is evaluated and returned.
#@author Infernos : CS699 Course Project Software Lab
#@date Thursday, November 29, 2019

##Include section
from Match_strings import plag_index_strings
import numpy as np

try:
    import pymysql

    pymysql.install_as_MySQLdb()
except ImportError:
    print('Install pymysql!')
    pass
db = pymysql.connect("localhost","wordpressuser","wordpressuser","wordpress" )
cursor = db.cursor()

##
#@brief This function is taking a filename as argument and returning a list of integers inside the file.
#@details The given file contains integers each line. This function is picking out text line by line, typecasting it to integers
#and appending it to a list. Finally it is returning that list.
#@return l list 
#@param filename the name of the file 
#
def plag_calc(parent_id, correct, marks, weight):
    test_id = parent_id
    roll = extract_roll(test_id)
    ques = extract_questions(test_id)
    ans = extract_answers(roll, ques)
    index_q = plag_ques_wise(roll, ques, ans, weight, correct)
    final_index = norm_final_index(index_q, marks)
    return final_index


##
#@brief This function is taking a test id as argument and returning a list of roll numbers attempted that test.
#@details Since test id field is not there in the table wp_postmeta, this function is extracting roll numbers by first extracting id 
# values corresponding to that test id and whose label is roll number or similar to it. Then using these id values roll numbers can be 
#extracted from wp_postmeta table. 
#@return roll_numbers list  
#@param test_id int test id
#
def extract_roll(test_id):
    cursor.execute(
        "SELECT id from wp_nf3_fields WHERE LOWER(label) LIKE 'roll%number' AND parent_id=" + str(test_id) + ";")
    # Fetch a single row using fetchone() method.
    roll_meta_key = '_field_' + str(list(cursor.fetchone())[0])
    cursor.execute("select meta_value from wp_postmeta where meta_key='%s'" % (roll_meta_key))
    roll_numbers = [i[0] for i in cursor.fetchall()]
    return roll_numbers

##
#@brief This function takes test id as argument and returns a list of list which consist of triplets id, label and type of each question.
#@details Function is executing a query and extracting only questions (Submit label and roll number are ignored) from the database corresponding to that 
#test. It is also storing the type of the question.
#@return questions list of lists  
#@param test_id int test id
#
def extract_questions(test_id):
    cursor.execute("SELECT id,label,type from wp_nf3_fields WHERE parent_id=" + str(
        test_id) + " and label!='Submit' and LOWER(label) NOT LIKE 'roll%number';")
    questions = [list(i) for i in cursor.fetchall()]
    for i in questions:
        i[0] = '_field_' + str(i[0])
    return questions


##
#@brief This function takes list of roll numbers as argument and returns a list of list which contains all answers.
#@details For each roll number answer is having a list in it which consist of this roll number's responses to all the questions of
#the test. Iterating the same way answer is list of lists which keeps the information of responses of all the roll numbers attempted
# this test
#@return answers list of lists contains all question's responses corresponding to all the roll numbers 
#@param roll list roll number 
#@param ques list of lists information about the question extracted from database

def extract_answers(roll, ques):
    answers = [[] for i in roll]
    for q in ques:
        cursor.execute("select meta_value from wp_postmeta where meta_key='%s'" % (q[0]))
        out = [i[0] for i in cursor.fetchall()]
        for i in range(len(out)):
            answers[i].append(out[i])
    return answers


##
#@brief Taking rollnumbers, questions, answers, weights and correct sols and returning the plagarism index.
#@details This function takes all nC2 combinations of the students who has taken the test and comparing their solutions with each other.
#And then evaluating a cheating index for that question. Also there is a progress bar at the end which shows the % of job finished.
#@return plag_index
#@param roll list All rollnumbers
#@param ques list All questions
#@param ans list All answers
#@param weight list Weights of algorithms
#@param correct list
def plag_ques_wise(roll, ques, ans, weight, correct):
    plag_index = [['Roll_1', 'Roll_2']]
    for i in ques:
        plag_index[0].append(i[1])
    plag_index[0].append('Overall_index')
    current_pair = 1
    nroll = len(roll)
    tottodo = nroll*(nroll-1)/2
    for i in range(nroll):
        for j in range(i + 1, nroll):
            plag_index.append([roll[i], roll[j]])
            for k in range(len(ques)):
                if ques[k][2] == 'textbox' or ques[k][2] == 'textarea':
                    plag_index[current_pair].append(plag_index_strings(ans[i][k], ans[j][k], weight))
                elif ques[k][2] == 'listradio':
                    if ans[i][k] == ans[j][k] and ans[i][k] != correct[k]:
                        plag_index[current_pair].append(1.0)
                    else:
                        plag_index[current_pair].append(0.0)
                elif ques[k][2] == 'listcheckbox':
                    ans1 = mult_corr_list(ans[i][k])
                    ans2 = mult_corr_list(ans[j][k])
                    if ans1 == ans2 and ans1 != correct[k]:
                        plag_index[current_pair].append(1.0)
                    else:
                        plag_index[current_pair].append(0.0)
                else:
                    plag_index[current_pair].append(0)
            print(str(round( current_pair*100/tottodo ,2))+'% done...')
            current_pair += 1
    return plag_index

##
#@brief This function takes plagiarism indices for individual questions and weight them according to the distribution of marks.
#@details For each pair of roll numbers there is a plagiarism index for each question. To get one normalised Plagiarism index, these
#indices are weighted according to the Question's marks distribution and It finally return us a final normalised Plagiarism Indices for
# all pairs.
#@return final list  Contains normalised plagiarism index for each pair of roll numbers
#@param index_x list Contains plagiarised index corresponding to each question for each pair of rollnumbers 
#@param marks list marks weightage given by the teacher to each question
def norm_final_index(index_q, marks):
    final = index_q[:]
    tot_marks = np.sum(np.array(marks))
    for i in range(1, len(final)):
        prod = np.sum(np.array(final[i][2:]) * np.array(marks))
        final[i].append(prod / tot_marks)
    return final

##
#@brief This function takes plagiarism indices for individual questions and weight them according to the distribution of marks.
#@return res 
#@param ans 

def mult_corr_list(ans):
    ll = ans.split('"')
    res = [ll[i] for i in range(len(ll)) if i % 2 != 0]
    res.sort()
    return res
