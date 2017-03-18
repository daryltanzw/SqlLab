import os

from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import FormView

from SqlLabApp.forms.createtest import CreateTestForm
from SqlLabApp.utils.DBUtils import get_db_connection
from SqlLabApp.utils.TestNameTableFormatter import test_name_table_format


class CreateTestFormView(FormView):
    form_class = CreateTestForm
    template_name = 'SqlLabApp/createtest_new.html'
    success_url = '/'

    def post(self, request, *args, **kwargs):
        create_test_form = self.form_class(request.POST, request.FILES)

        if create_test_form.is_valid():

            # create_TestForClass_row(classid, starttime, endtime, max_attempt, test_name), return tid

            q_a_file_name = request.FILES['q_a_file_upload'].name
            q_a_file_lines = request.FILES['q_a_file_upload'].read().splitlines()

            data_file = request.FILES['data_file_upload']

            validate_msg_q_a_file = validate_q_a_file(q_a_file_name, q_a_file_lines)
            if validate_msg_q_a_file != "Valid":
                return HttpResponse(validate_msg_q_a_file)



            # validate data_file parsing..
            # try run sql code

            # create_test_name_table(test_name_table_format(tid, test_name)
            # if not create_test_name_table(test_name_table_format(1, request.POST['test_name']),
            #                               q_a_file_lines):
            #     return HttpResponse("Unable to Create test_name Database")
            # Can try raise exception so the 3 table creations with the DB is in one transaction!

            # create QuestionDataUsedByTest and dynamic data_tbl_name from the .sql
        else:
            return HttpResponse("Create Test Not Successful! Please Contact Dev")

        return HttpResponseRedirect("../instructormodule")


def validate_q_a_file(filename, q_a_file_lines):
    file_ext = os.path.splitext(filename)[1]
    valid_extensions = ['.tsv', '.txt']

    if file_ext.lower() not in valid_extensions:
        return "Only tsv or txt files are allowed"

    for row in q_a_file_lines:
        splitted = row.split("\t")
        if len(splitted) != 2:
            return "Expected 2 columns with one tab separation -> {0}".format(row)

    return "Valid"


# assumes tbl_name has been formatted using utils/QuestionTableFormatter
def create_test_name_table(tbl_name, q_a_file_lines):
    try:
        db_conn = get_db_connection()
        cursor = db_conn.cursor()

        cursor.execute("drop table if exists {0};".format(tbl_name))
        cursor.execute(
            "create table {0} (qid INTEGER primary key, question text, teacher_answer text);".format(tbl_name))

        q_no = 0
        for row in q_a_file_lines:
            r = row.split("\t")
            q_no += 1
            cursor.execute("Insert into {0} values({1},%s, %s)"
                           .format(tbl_name, q_no), (r[0], r[1]))
            # sqltable, q1, question text, answer text
            # %s %s is the database to avoid quotes as the queries inserted as text will containt quotes

        db_conn.commit()
        return True

    except:
        return False
