import itertools as it

from django.views.generic import FormView
from django.db import connection

from SqlLabApp.forms.taketest import TakeTestForm
from SqlLabApp.models import QuestionAnswer, TestForClass, QuestionDataUsedByTest
from SqlLabApp.utils.TestNameTableFormatter import test_name_table_format
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

    # def post(self, request, *args, **kwargs):
    #     take_test_form = self.form_class(request.POST)
    #     if take_test_form.is_valid():
    #         take_test_form.save(request.user)
    #         return HttpResponseRedirect("../instructormodule")
    #
    #     else:
    #         return self.render_to_response(
    #             self.get_context_data(
    #                 take_test_form=take_test_form,
    #             )
    #         )
