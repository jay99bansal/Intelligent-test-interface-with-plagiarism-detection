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


def plag_calc(parent_id, correct, marks, weight):
    test_id = parent_id
    roll = extract_roll(test_id)
    ques = extract_questions(test_id)
    ans = extract_answers(roll, ques)
    index_q = plag_ques_wise(roll, ques, ans, weight, correct)
    final_index = norm_final_index(index_q, marks)
    return final_index


def extract_roll(test_id):
    cursor.execute(
        "SELECT id from wp_nf3_fields WHERE LOWER(label) LIKE 'roll%number' AND parent_id=" + str(test_id) + ";")
    # Fetch a single row using fetchone() method.
    roll_meta_key = '_field_' + str(list(cursor.fetchone())[0])
    cursor.execute("select meta_value from wp_postmeta where meta_key='%s'" % (roll_meta_key))
    roll_numbers = [i[0] for i in cursor.fetchall()]
    return roll_numbers


def extract_questions(test_id):
    cursor.execute("SELECT id,label,type from wp_nf3_fields WHERE parent_id=" + str(
        test_id) + " and label!='Submit' and LOWER(label) NOT LIKE 'roll%number';")
    questions = [list(i) for i in cursor.fetchall()]
    for i in questions:
        i[0] = '_field_' + str(i[0])
    return questions


def extract_answers(roll, ques):
    answers = [[] for i in roll]
    for q in ques:
        cursor.execute("select meta_value from wp_postmeta where meta_key='%s'" % (q[0]))
        out = [i[0] for i in cursor.fetchall()]
        for i in range(len(out)):
            answers[i].append(out[i])
    return answers


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


def norm_final_index(index_q, marks):
    final = index_q[:]
    tot_marks = np.sum(np.array(marks))
    for i in range(1, len(final)):
        prod = np.sum(np.array(final[i][2:]) * np.array(marks))
        final[i].append(prod / tot_marks)
    return final


def mult_corr_list(ans):
    ll = ans.split('"')
    res = [ll[i] for i in range(len(ll)) if i % 2 != 0]
    res.sort()
    return res
