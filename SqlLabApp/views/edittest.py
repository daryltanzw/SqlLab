import os

import sqlparse
from django.db import transaction
from django.http import HttpResponseRedirect
from django.views.generic import FormView
from SqlLabApp.models import TestForClass
from SqlLabApp.forms.edittest import EditTestForm
from SqlLabApp.models import User, TestForClass, QuestionDataUsedByTest
from SqlLabApp.utils.CreateTestDataParser import get_tbl_names, append_to_relations
from SqlLabApp.utils.CreateTestNameTable import create_test_name_table
from SqlLabApp.utils.DBUtils import get_db_connection
from SqlLabApp.utils.TestNameTableFormatter import test_name_table_format

from django.shortcuts import render
from SqlLabApp.utils.CryptoSign import decryptData

class EditTestFormView(FormView):
    form_class = EditTestForm
    template_name = 'SqlLabApp/edittest.html'
    success_url = '/'

    def get(self, request, *args, **kwargs):
        test_id = self.kwargs['test_id']
        tid = int(decryptData(test_id))

        test = TestForClass.objects.get(tid=tid)
        form = EditTestForm(instance=test)

        full_name = User.objects.get(email=request.user.email).full_name

        test.tid = test_id
        return render(request, self.template_name, {'form': form, 'test': test, 'full_name': full_name})

    def post(self, request, *args, **kwargs):
        edit_test_form = self.form_class(request.POST)
        test_id = self.kwargs['test_id']
        tid = int(decryptData(test_id))

        if edit_test_form.is_valid():
            if edit_test_form.has_changed():
                start_time = request.POST['start_time']
                end_time = request.POST['end_time']
                max_attempt = request.POST['max_attempt']
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
                        connection.commit()

                except ValueError as err:
                    connection.close()
                    raise err

                return HttpResponseRedirect("../test")

            else:
                return HttpResponseRedirect("../test")
        else:
            raise ValueError(edit_test_form.errors)
