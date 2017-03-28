from django.db import transaction
from django.http import HttpResponseRedirect
from django.views import View

from SqlLabApp.models import Class
from SqlLabApp.utils.DBUtils import get_db_connection

from django.shortcuts import render
from SqlLabApp.utils.CryptoSign import decryptData


class DeleteModuleView(View):
    success_url = '/'

    def get(self, request, *args, **kwargs):
        cid = self.kwargs['class_id']
        class_id = int(decryptData(cid))

        try:
            connection = get_db_connection()
            with transaction.atomic():
                module = Class.objects.get(classid=class_id)
                module.delete()
                connection.commit()

        except ValueError as err:
            connection.close()
            raise err

        return HttpResponseRedirect("../../module")
