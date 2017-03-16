from django.views.generic import FormView
import csv
from SqlLabApp.forms.createtest import CreateTestForm
from SqlLabApp.utils.DBUtils import get_db_connection


class CreateTestFormView(FormView):
    form_class = CreateTestForm
    template_name = 'SqlLabApp/createtest.html'
    success_url = '/'


# assumes tbl_name has been formatted using utils/QuestionTableFormatter
def create_question_table(tbl_name, q_a_absfilepath):
    try:
        db_conn = get_db_connection()
        cursor = db_conn.cursor()

        cursor.execute("drop table if exists {0};".format(tbl_name))
        cursor.execute(
            "create table {0} (qid INTEGER primary key, question text, teacher_answer text);".format(tbl_name))

        with open(q_a_absfilepath) as f:
            reader = csv.reader(f, delimiter='\t')
            qNo = 0
            if __name__ == '__main__':
                for row in reader:
                    qNo += 1
                    cursor.execute("Insert into {0} values({1},%s, %s)"
                                   .format(tbl_name, qNo), (row[0], row[1]))
                    # sqltable, q1, question text, answer text
                    # %s %s is the database to avoid quotes as the queries inserted as text will containt quotes

        db_conn.commit()
        return True

    except:
        return False
