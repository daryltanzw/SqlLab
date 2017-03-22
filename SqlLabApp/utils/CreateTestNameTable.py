# assumes tbl_name has been formatted using utils/TestNameTableFormatter
def create_test_name_table(cursor, tbl_name, q_a_file_lines):
    try:
        cursor.execute("drop table if exists {0};".format(tbl_name))
        cursor.execute(
            "create table {0} (qid INTEGER primary key, question text, teacher_answer text, marks INTEGER);".format(tbl_name))

        q_no = 0
        for row in q_a_file_lines:
            r = row.split("\t")
            q_no += 1
            cursor.execute("Insert into {0} values(%s, %s, %s, %s)".format(tbl_name), (q_no, r[0], r[1], r[2]))
            # sqltable, q1, question text, answer text
            # %s %s is the database to avoid quotes as the queries inserted as text will containt quotes

    except Exception as err:
        raise ValueError(err)
