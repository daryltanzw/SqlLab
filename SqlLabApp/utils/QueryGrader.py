import re

import sqlparse
from sqlparse.sql import Identifier, IdentifierList
from SqlLabApp.utils.DBUtils import get_db_connection

from SqlLabApp.utils.TestNameTableFormatter import test_name_table_format


def grade_formatted_query(student_query, teacher_query, mark):
    default_mark = 0

    try:
        conn = get_db_connection()
        fq1 = student_query.replace(";", "")
        fq2 = teacher_query.replace(";", "")

        with conn.cursor() as cursor:
            query = "( %s Except %s) UNION ALL (%s EXCEPT %s)" % (fq1, fq2, fq2, fq1)
            cursor.execute(query)
            r = cursor.fetchall()

            if len(r) != 0:
                mark = default_mark

    except:
        mark = default_mark

    finally:
        conn.close()
        return mark


def format_query(tid, query_str):
    formatted_query = query_str
    table_name_list = get_tbl_names_from_select_query(query_str)
    table_dict = table_name_to_formatted(tid, table_name_list)

    for key in table_dict.keys():
        if key in query_str:
            formatted_query = str(re.sub(r'\b{0}\b'.format(key), table_dict.get(key), formatted_query)).strip()

    return formatted_query


def get_tbl_names_from_select_query(query_str):
    result = sqlparse.parse(sqlparse.format(query_str, reindent=True, keyword_case='upper'))[0]

    table_name_list = []
    toReturn = []
    if result.token_first().value == 'SELECT':
        for token in result.tokens:
            if isinstance(token, IdentifierList) or isinstance(token, Identifier):
                table_name_list = token.value.splitlines()

    for name in table_name_list:
        s = str(name).strip().split(None, 1)[0]
        toReturn.append(s)

    return toReturn


def table_name_to_formatted(tid, table_name_list):
    table_dict = {}
    for name in table_name_list:
        table_dict[name] = str(test_name_table_format(tid, name))

    return table_dict
