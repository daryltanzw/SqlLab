import datetime
import time

from django.views.generic import FormView
from django.db import connection
from django.db import transaction
from SqlLabApp.forms.test import InstructorTestForm
from django.http import HttpResponseRedirect

from SqlLabApp.models import User, UserRole, Class, TestForClass, StudentAttemptsTest
from SqlLabApp.utils.DBUtils import get_db_connection
from SqlLabApp.utils.CryptoSign import encryptData
from SqlLabApp.utils.CryptoSign import decryptData

class InstructorTestFormView(FormView):
    form_class = InstructorTestForm
    template_name = 'SqlLabApp/test.html'
    success_url = '/'

    def get(self, request, *args, **kwargs):
        cid = self.kwargs['class_id']
        classid = int(decryptData(cid))

        module_name = Class.objects.get(classid=classid).class_name
        create_module_form = InstructorTestForm
        tests = TestForClass.objects.filter(classid_id=classid).order_by('test_name')
        attempts = []
        can_take_test = []

        for tobj in tests:
            curr_attempt = StudentAttemptsTest.objects.filter(tid_id=tobj.tid, student_email_id=request.user.email).count()
            attempts.append(curr_attempt)
            current_time = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
            end_time = datetime.datetime.strftime(tobj.end_time, '%Y-%m-%d %H:%M:%S')

            if curr_attempt < tobj.max_attempt and current_time <= end_time:
                can_take_test.append(True)
            else:
                can_take_test.append(False)

            tobj.tid = encryptData(tobj.tid)

        user_role = UserRole.objects.get(email_id=request.user.email).role
        full_name = User.objects.get(email=request.user.email).full_name
        test_list = zip(tests, can_take_test, attempts)

        return self.render_to_response(
            self.get_context_data(
                full_name=full_name,
                user_role=user_role,
                classid=cid,
                test_list=test_list,
                module_name=module_name,
                create_module_form=create_module_form,
            )
        )

