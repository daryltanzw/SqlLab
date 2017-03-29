from django.views.generic import FormView
from SqlLabApp.forms.test import InstructorTestForm

from SqlLabApp.models import UserRole, Class, TestForClass
from SqlLabApp.utils.CryptoSign import encryptData
from SqlLabApp.utils.CryptoSign import decryptData

class InstructorTestFormView(FormView):
    model = Class
    form_class = InstructorTestForm
    template_name = 'SqlLabApp/test.html'
    success_url = '/'

    def get(self, request, *args, **kwargs):
        cid = self.kwargs['class_id']
        classid = int(decryptData(cid))

        module_name = Class.objects.get(classid=classid).class_name
        create_module_form = InstructorTestForm
        test_list = TestForClass.objects.filter(classid_id=classid).order_by('test_name')

        for tobj in test_list:
            tobj.tid = encryptData(tobj.tid)

        user_role = UserRole.objects.get(email_id=request.user.email).role


        return self.render_to_response(
            self.get_context_data(
                user_role=user_role,
                classid=cid,
                test_list=test_list,
                module_name=module_name,
                create_module_form=create_module_form,
            )
        )