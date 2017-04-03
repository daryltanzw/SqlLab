from django.db import transaction
from django.http import HttpResponseRedirect
from django.views.generic import FormView
from SqlLabApp.forms.editvisibility import EditVisibilityForm
from SqlLabApp.models import TestForClass, QuestionDataUsedByTest
from SqlLabApp.utils.DBUtils import get_db_connection

from django.shortcuts import render
from SqlLabApp.utils.CryptoSign import encryptData
from SqlLabApp.utils.CryptoSign import decryptData


class EditVisibilityFormView(FormView):
    form_class = EditVisibilityForm
    template_name = 'SqlLabApp/editvisibility.html'
    success_url = '/'

    def get(self, request, *args, **kwargs):
        test_id = self.kwargs['test_id']
        tid = int(decryptData(test_id))

        data_tables = QuestionDataUsedByTest.objects.filter(tid_id=tid)
        data_table_names = []

        for table in data_tables:
            data_table_names.append(table.data_tbl_name)

        form = EditVisibilityForm(dynamic_field_names=data_table_names)

        return render(request, self.template_name, {'form': form, 'data_tables': data_tables})

    def post(self, request, *args, **kwargs):
        edit_visibility_form = self.form_class(request.POST)
        test_id = self.kwargs['test_id']
        tid = int(decryptData(test_id))
        class_id = encryptData(TestForClass.objects.get(tid=tid).classid_id)

        # if edit_visibility_form.is_valid():
        # if edit_visibility_form.has_changed():
        data_tables = QuestionDataUsedByTest.objects.filter(tid_id=tid)

        try:
            connection = get_db_connection()
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

        #     else:
        #         return HttpResponseRedirect("../../" + str(class_id) + "/test")
        #
        # else:
        #     raise ValueError(edit_visibility_form.errors)
