from django.db import transaction
from django.http import HttpResponseRedirect
from django.views.generic import FormView

from SqlLabApp.forms.editmodule import EditModuleForm
from SqlLabApp.models import Class
from SqlLabApp.utils.DBUtils import get_db_connection

from django.shortcuts import render


class EditModuleFormView(FormView):
    form_class = EditModuleForm
    template_name = 'SqlLabApp/editmodule.html'
    success_url = '/'

    def get(self, request, *args, **kwargs):
        cid = self.kwargs['class_id']
        print "========================================"
        print cid
        class_id = int(cid[0])
        print class_id
        module = Class.objects.get(classid=class_id)
        form = EditModuleForm(instance=module)
        return render(request, self.template_name, {'form': form, 'module': module})

    def post(self, request, *args, **kwargs):
            edit_module_form = self.form_class(request.POST)
            cid = self.kwargs['class_id']
            class_id = int(cid[0])

            if edit_module_form.is_valid():
                if edit_module_form.has_changed():
                    class_name = request.POST['class_name']
                    semester = request.POST['semester']
                    facilitators = request.POST['facilitators']
                    try:
                        connection = get_db_connection()
                        with transaction.atomic():
                            module = Class.objects.get(classid=class_id)
                            queryset_module = Class.objects.filter(classid=class_id)
                            fields = ['class_name', 'semester', 'facilitators']
                            updatedValues = [class_name, semester, facilitators]
                            for field, updatedValue in zip(fields, updatedValues):
                                if getattr(module, field) != updatedValue:
                                    queryset_module.update(**{field: updatedValue})
                            connection.commit()

                    except ValueError as err:
                        connection.close()
                        raise err

                    return HttpResponseRedirect("../../module")

                else:
                    return HttpResponseRedirect("../../module")
            else:
                raise ValueError(edit_module_form.errors)