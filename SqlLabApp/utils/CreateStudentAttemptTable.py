import itertools as it

from SqlLabApp.models import TestForClass
from SqlLabApp.utils.CorrectnessChecker import compare
from SqlLabApp.utils.TestNameTableFormatter import test_name_table_format

def create_student_attempt_table(cursor, tbl_name, tid, student_answer_list):
    try:
        cursor.execute("drop table if exists {0};".format(tbl_name))
        cursor.execute(
            "create table {0} (qid INTEGER primary key, question text, student_answer text, marks INTEGER);".format(tbl_name))

        q_no = 0
        for student_answer in student_answer_list:
            q_no += 1
            test_name = TestForClass.objects.get(tid=tid).test_name
            test_table = test_name_table_format(tid, test_name).lower()

            # Retrieve question from test table
            cursor.execute('select question, teacher_answer, marks from ' + test_table + ' where qid = ' + str(q_no))
            tuple_list = cursor.fetchone()
            question = tuple_list[0]
            instructor_answer = tuple_list[1]
            total_marks = tuple_list[2]

            # Mark student's query against instructor's query
            # TODO: Replace query's table names with actual table names stored
            correctness = compare(instructor_answer.replace(";", ""), student_answer.replace(";", ""))
            student_marks = 0

            # Correct = full marks, wrong = 0
            if correctness == 0:
                student_marks = total_marks

            cursor.execute("Insert into {0} values(%s, %s, %s, %s)".format(tbl_name), (q_no, question, student_answer, student_marks))

    except Exception as err:
        raise ValueError(err)
