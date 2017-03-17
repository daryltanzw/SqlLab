import csv
import os
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import FormView
from SqlLabApp.forms.createtest import CreateTestForm
from SqlLabApp.utils.DBUtils import get_db_connection


class CreateTestFormView(FormView):
    form_class = CreateTestForm
    template_name = 'SqlLabApp/createtest_new.html'
    success_url = '/'

    def post(self, request, *args, **kwargs):
        create_test_form = self.form_class(request.POST, request.FILES)

        if create_test_form.is_valid():
            # create_TestForClass_row(classid, starttime, endtime, max_attempt, test_name), return tid

            q_a_file = request.FILES['q_a_file_upload']
            data_file = request.FILES['data_file_upload']

            validate_msg_q_a_file = validate_q_a_file(q_a_file)
            if validate_msg_q_a_file != "Valid":
                return HttpResponse(validate_msg_q_a_file)

            # validate data_file parsing..
            # try run sql code

            # create_test_name_table(test_name_table_format(tid, test_name)
            # create QuestionDataUsedByTest and dynamic data_tbl_name from the .sql
        else:
            return HttpResponse("Create Test Not Successful! Please Contact Dev")

        return HttpResponseRedirect("../instructor")


def validate_q_a_file(q_a_file):
    file_ext = os.path.splitext(q_a_file.name)[1]
    valid_extensions = ['.tsv', '.txt']

    if file_ext.lower() not in valid_extensions:
        return "Only tsv or txt files are allowed"

    for row in q_a_file.readlines():
        splitted = row.split("\t")
        if len(splitted) != 2:
            return "Incorrect Question&Answer Content. Format -> {Question \'tab\' Answer}"

    return "Valid"


# assumes tbl_name has been formatted using utils/QuestionTableFormatter
def create_test_name_table(tbl_name, q_a_absfilepath):
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
