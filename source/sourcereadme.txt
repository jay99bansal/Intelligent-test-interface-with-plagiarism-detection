**************************************
How to run the project?
**************************************

************ Front end *****************

Create wordpress project as directed in the demo, if you don't have wordpress installed and just want to test the plagiarism detection tool, we have given databse wordpress.sql in this folder which can be dumped into your mysql and then the python scripts are ready to use!

mysql -u username -p dbname < wordpress.sql

*********** Back end *****************

When all the students have submitted their responses, the instructor just need to run generate_csv.py which generates a csv file plagiarism.csv in the same directory which contains all the plagiarism indices for each pair of students for each question and cummulative index for a pair in the test in decreasing order. To run this file, the instuctor needs to give testID, solutions(solutions and marks of all questions) and weights for all 4 plagiarism detecting algorithms as input. Solutions and marks being csv files whose examples can be seen in the same directory!

python3 generate_csv.py --testID testid --solutions path/to/solutions --weights path/of/weights

An example to this will look like:

pyhton3 generate_csv.py --testID 3 --solutions /home/jay/Desktop/solutions.csv --weights /home/jay/Desktop/weights.csv

This will generate final csv output named plagiarism.py(An example is already submitted in the same directory)!

****************************************
