from django.db import transaction
from django.http import HttpResponseRedirect
from django.views import View

from SqlLabApp.models import TestForClass
from SqlLabApp.utils.DBUtils import get_db_connection

from SqlLabApp.utils.CryptoSign import encryptData
from SqlLabApp.utils.CryptoSign import decryptData


class DeleteTestView(View):
    success_url = '/'

    def get(self, request, *args, **kwargs):
        test_id = self.kwargs['test_id']
        tid = int(decryptData(test_id))
        class_id = encryptData(TestForClass.objects.get(tid=tid).classid_id)

        try:
            connection = get_db_connection()
            with transaction.atomic():
                test = TestForClass.objects.get(tid=tid)
                test.delete()
                connection.commit()

        except ValueError as err:
            connection.close()
            raise err

        return HttpResponseRedirect("../../" + str(class_id) + "/test")
