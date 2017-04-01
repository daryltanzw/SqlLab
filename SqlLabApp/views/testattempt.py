from django.views.generic import FormView
from SqlLabApp.forms.testattempt import TestAttemptForm

from SqlLabApp.models import User, UserRole, TestForClass, StudentAttemptsTest
from SqlLabApp.utils.CryptoSign import encryptData
from SqlLabApp.utils.CryptoSign import decryptData

class TestAttemptFormView(FormView):
    form_class = TestAttemptForm
    template_name = 'SqlLabApp/testattempt.html'
    success_url = '/'

    def get(self, request, *args, **kwargs):
        tid = self.kwargs['test_id']
        testid = int(decryptData(tid))

        test_attempt_list = StudentAttemptsTest.objects.filter(tid_id=testid,student_email_id=request.user.email)
        test_name = TestForClass.objects.get(tid=testid).test_name
        user_role = UserRole.objects.get(email_id=request.user.email).role
        full_name = User.objects.get(email=request.user.email).full_name

        for tobj in test_attempt_list:
            tobj.tid_id = encryptData(tobj.tid_id)

        return self.render_to_response(
            self.get_context_data(
                full_name=full_name,
                user_role=user_role,
                testid=tid,
                test_name=test_name,
                test_attempt_list=test_attempt_list
            )
        )