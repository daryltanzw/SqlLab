from SqlLabApp.models import TestForClass

from SqlLabApp.utils.TestNameTableFormatter import test_name_table_format
import SqlLabApp.utils.QueryGrader as grader


def create_student_attempt_table(cursor, tbl_name, tid, student_answer_list):
    try:
        cursor.execute("drop table if exists {0};".format(tbl_name))
        cursor.execute(
            "create table {0} (qid INTEGER primary key, question text, student_answer text, marks INTEGER);".format(
                tbl_name))

        q_no = 0
        for student_answer in student_answer_list:
            q_no += 1
            test_name = TestForClass.objects.get(tid=tid).test_name
            test_table = test_name_table_format(tid, test_name).lower()

            # Retrieve question from test table
            cursor.execute('select question, teacher_answer, marks from ' + test_table + ' where qid = ' + str(q_no))
            tuple_list = cursor.fetchone()
            question = str(tuple_list[0])
            instructor_answer = str(tuple_list[1])
            total_marks = tuple_list[2]

            # Mark student's query against instructor's query
            student_query = grader.format_select_query(tid, student_answer)
            teacher_query = grader.format_select_query(tid, instructor_answer)
            marks_obtained = grader.grade_formatted_query(student_query, teacher_query, total_marks)

            cursor.execute("Insert into {0} values(%s, %s, %s, %s)".format(tbl_name), (
            q_no, question, student_answer, marks_obtained))

    except Exception as err:
        raise ValueError(err)
