from SqlLabApp.forms.instructormodule import InstructorModuleForm, CreateModuleForm
from django.http import HttpResponseRedirect
from django.views.generic import FormView


class CreateModuleFormView(FormView):
    form_class = CreateModuleForm
    template_name = 'SqlLabApp/instructormodule.html'
    success_url = '/'

    def post(self, request, *args, **kwargs):
        # instructor_form = InstructorModuleForm()
        create_module_form = self.form_class(request.POST)
        if create_module_form.is_valid():
            create_module_form.save(request.user)
            return HttpResponseRedirect("../instructormodule")

        else:
            return self.render_to_response(
                self.get_context_data(
                    create_module_form=create_module_form,

                )
            )


# class InstructorModuleFormView(FormView):
    # form_class = InstructorModuleForm
    # template_name = 'SqlLabApp/instructormodule.html'
    # success_url = '/'

    # def post(self, request, *args, **kwargs):
    #     create_module_form = CreateModuleForm()
    #     instructor_form = self.form_class(request.POST)
    #     if instructor_form.is_valid():
    #         # instructor_form.save(request.user)
    #         return HttpResponseRedirect("../instructormodule")
    #
    #     else:
    #         return self.render_to_response(
    #                 self.get_context_data(
    #                     instructor_form=instructor_form,
    #                     create_module_form=create_module_form
    #                 )
    #             )