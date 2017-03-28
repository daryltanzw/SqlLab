import itertools as it

from django.views.generic import FormView
from django.db import connection
from django.db import transaction
from django.http import HttpResponseRedirect

from SqlLabApp.forms.taketest import TakeTestForm
from SqlLabApp.models import QuestionAnswer, TestForClass, StudentAttemptsTest, QuestionDataUsedByTest
from SqlLabApp.utils.TestNameTableFormatter import test_name_table_format, student_attempt_table_format
from SqlLabApp.utils.CreateStudentAttemptTable import create_student_attempt_table
from SqlLabApp.utils.DBUtils import get_db_connection
from SqlLabApp.utils.CryptoSign import decryptData


class TakeTestFormView(FormView):
    form_class = TakeTestForm
    template_name = 'SqlLabApp/taketest.html'
    success_url = '/'

    def get(self, request, *args, **kwargs):
        test_id = self.kwargs['test_id']
        tid = int(decryptData(test_id))

        take_test_form = TakeTestForm
        test_name = TestForClass.objects.get(tid=tid).test_name
        test_name_table = test_name_table_format(tid, test_name)
        qst_data = QuestionAnswer.objects.raw('SELECT * FROM ' + test_name_table)

        # Retrieve all tables used by current test
        table_names = QuestionDataUsedByTest.objects.filter(tid_id=tid, student_visibility='t')
        tables = []

        for table in table_names:
            with connection.cursor() as cursor:
                # Get table name
                table_name = 'tid' + str(tid) + '_' + table.data_tbl_name

                # Retrieve column names
                cursor.execute(
                    'SELECT column_name FROM information_schema.columns WHERE table_name=\'' + table_name + '\'')
                curr_table_columns = [tuple(i[0] for i in it.chain(cursor.fetchall()))]

                # Retrieve current table data
                cursor.execute('SELECT * FROM ' + table_name)
                curr_table_rows = cursor.fetchall()

                # Remove tid from table name
                table_name = table_name.split("_", 1)[1]
                name = [table_name]
                tables.append(curr_table_columns + curr_table_rows + name)

        return self.render_to_response(
            self.get_context_data(
                tables=tables,
                take_test_form=take_test_form,
                test_name=test_name,
                qst_data=qst_data,
            )
        )

    def post(self, request, *args, **kwargs):
        submit_answer_form = self.form_class(request.POST)
        test_id = self.kwargs['test_id']
        tid = int(decryptData(test_id))

        if submit_answer_form.is_valid():
            student_answer_list = request.POST.getlist('student_answer')
            student_email = request.user.email
            attempt_no = StudentAttemptsTest.objects.filter(tid_id=tid, student_email_id=student_email).count() + 1

            try:
                connection = get_db_connection()
                with transaction.atomic():
                    student_attempt_test_row = StudentAttemptsTest(attempt_no=attempt_no, student_email_id=student_email,
                                                                   tid_id=tid)
                    student_attempt_test_row.save()
                    cursor = connection.cursor()
                    create_student_attempt_table(cursor, student_attempt_table_format(tid, student_email, attempt_no), tid,
                                                 student_answer_list)
                    connection.commit()

            except ValueError as err:
                connection.close()
                raise err

            return HttpResponseRedirect("../test")

        else:
            raise ValueError(submit_answer_form.errors)
