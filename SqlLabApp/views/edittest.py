import datetime
import time

from django.db import transaction
from django.http import HttpResponseRedirect
from django.views.generic import FormView
from SqlLabApp.forms.edittest import EditTestForm
from SqlLabApp.models import User, TestForClass, QuestionDataUsedByTest
from SqlLabApp.utils.DBUtils import get_db_connection

from django.shortcuts import render
from SqlLabApp.utils.CryptoSign import encryptData
from SqlLabApp.utils.CryptoSign import decryptData


class EditTestFormView(FormView):
    form_class = EditTestForm
    template_name = 'SqlLabApp/edittest.html'
    success_url = '/'

    def get(self, request, *args, **kwargs):
        test_id = self.kwargs['test_id']
        tid = int(decryptData(test_id))

        test = TestForClass.objects.get(tid=tid)
        full_name = User.objects.get(email=request.user.email).full_name

        data_tables = QuestionDataUsedByTest.objects.filter(tid_id=tid)
        data_table_names = []

        for table in data_tables:
            data_table_names.append({'name': table.data_tbl_name, 'visibility': table.student_visibility})

        form = EditTestForm(instance=test, dynamic_field_names=data_table_names)
        test.tid = test_id

        return render(request, self.template_name, {'form': form,
                                                    'test': test,
                                                    'full_name': full_name,
                                                    'data_tables': data_tables})

    def post(self, request, *args, **kwargs):
        test_id = self.kwargs['test_id']
        tid = int(decryptData(test_id))
        class_id = encryptData(TestForClass.objects.get(tid=tid).classid_id)

        start_time = request.POST['start_time']
        end_time = request.POST['end_time']
        max_attempt = request.POST['max_attempt']
        data_tables = QuestionDataUsedByTest.objects.filter(tid_id=tid)

        current_time = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

        if end_time > current_time and start_time < end_time:
            try:
                connection = get_db_connection()
                with transaction.atomic():
                    test = TestForClass.objects.get(tid=tid)
                    queryset_test = TestForClass.objects.filter(tid=tid)
                    fields = ['start_time', 'end_time', 'max_attempt']
                    updatedValues = [start_time, end_time, max_attempt]

                    for field, updatedValue in zip(fields, updatedValues):
                        if getattr(test, field) != updatedValue:
                            queryset_test.update(**{field: updatedValue})

                    for table in data_tables:
                        result = request.POST.getlist(table.data_tbl_name)

                        with transaction.atomic():
                            is_visible = False
                            result = ''.join(result)
                            if result == 'on':
                                is_visible = True

                            QuestionDataUsedByTest.objects.filter(tid_id=tid, data_tbl_name=table.data_tbl_name).update(
                                student_visibility=is_visible)

                    connection.commit()

            except ValueError as err:
                connection.close()
                raise err

            return HttpResponseRedirect("../../" + str(class_id) + "/test")

        else:
            raise ValueError('Date cannot be in the past or start date cannot be before end date.')