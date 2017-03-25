from django.db import transaction
from django.http import HttpResponseRedirect
from django.views import View

from SqlLabApp.models import TestForClass
from SqlLabApp.utils.DBUtils import get_db_connection

from django.shortcuts import render


class DeleteTestView(View):
    success_url = '/'

    def get(self, request, *args, **kwargs):
        tid = self.kwargs['test_id']

        try:
            connection = get_db_connection()
            with transaction.atomic():
                test = TestForClass.objects.get(tid=tid)
                test.delete()
                connection.commit()

        except ValueError as err:
            connection.close()
            raise err

        return HttpResponseRedirect("../test")
