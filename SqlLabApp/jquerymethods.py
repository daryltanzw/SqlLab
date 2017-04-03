import json

from django.http import HttpResponse

import SqlLabApp.utils.QueryGrader as grader
from SqlLabApp.utils.CryptoSign import decryptData


def execute_query(request, *args, **kwargs):
    if request.method == 'GET':
        query = request.GET.get('query')
        test_id = kwargs['test_id']
        tid = int(decryptData(test_id))
        print("++++++++++++++++++++++++")
        print(tid)
        fq = grader.format_select_query(tid, query)
        result = grader.execute_formatted_query(fq)
        data = {"result": result}
        return HttpResponse(
            json.dumps(data),
            content_type="application/json"
        )

    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

