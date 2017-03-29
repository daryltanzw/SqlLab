import os

import sqlparse
from django.db import transaction
from django.http import HttpResponseRedirect
from django.views.generic import FormView

from SqlLabApp.forms.createtest import CreateTestForm
from SqlLabApp.models import TestForClass, QuestionDataUsedByTest
from SqlLabApp.utils.CreateTestDataParser import get_tbl_names, append_to_relations
from SqlLabApp.utils.CreateTestNameTable import create_test_name_table
from SqlLabApp.utils.DBUtils import get_db_connection
from SqlLabApp.utils.TestNameTableFormatter import test_name_table_format
from SqlLabApp.utils.CryptoSign import decryptData


class CreateTestFormView(FormView):
    form_class = CreateTestForm
    template_name = 'SqlLabApp/createtest.html'
    success_url = '/'

    def post(self, request, *args, **kwargs):
        create_test_form = self.form_class(request.POST, request.FILES)
        cid = self.kwargs['class_id']
        classid = int(decryptData(cid))

        if create_test_form.is_valid():
            start_time = request.POST['start_time']
            end_time = request.POST['end_time']
            max_attempt = request.POST['max_attempt']
            test_name = request.POST['test_name']
            q_a_file = request.FILES['q_a_file_upload']
            data_file = request.FILES['data_file_upload']

            if q_a_file is None or data_file is None:
                raise ValueError("No Upload for Q&A file or Data Files")

            q_a_file_lines = q_a_file.read().splitlines()
            data_file_lines = data_file.read().splitlines()

            try:
                connection = get_db_connection()
                with transaction.atomic():
                    test_for_class_row = TestForClass(classid_id=classid, max_attempt=max_attempt, test_name=test_name,
                                                      start_time=start_time, end_time=end_time)
                    test_for_class_row.save()
                    tid = test_for_class_row.tid

                    validate_q_a_file(q_a_file.name, q_a_file_lines)
                    cursor = connection.cursor()
                    processed_data_file_lines = append_to_relations(tid, data_file_lines)
                    run_sql(cursor, processed_data_file_lines)
                    create_test_name_table(cursor, test_name_table_format(tid, test_name), q_a_file_lines)
                    connection.commit()

                    data_tbl_name_list = get_tbl_names(data_file_lines)
                    for name in data_tbl_name_list:
                        question_data_used_by_test_row = QuestionDataUsedByTest(tid_id=tid, data_tbl_name=name)
                        question_data_used_by_test_row.save()

            except ValueError as err:
                connection.close()
                raise err

            return HttpResponseRedirect("../test")

        else:
            raise ValueError(create_test_form.errors)


def validate_q_a_file(filename, q_a_file_lines):
    file_ext = os.path.splitext(filename)[1]
    valid_extensions = ['.tsv', '.txt']

    if file_ext.lower() not in valid_extensions:
        raise ValueError("Only tsv or txt files are allowed")

    for row in q_a_file_lines:
        splitted = row.split("\t")
        if len(splitted) != 3:
            raise ValueError("Expected Question <tab> Answer <tab> Marks".format(row))


def run_sql(cursor, processed_data_file_lines):
    try:
        query = '\n'.join(processed_data_file_lines)
        result_list = sqlparse.parse(sqlparse.format(query, reindent=True, keyword_case='upper'))

        for result in result_list:
            cursor.execute(str(result))

    except Exception as err:
        raise ValueError(err)
