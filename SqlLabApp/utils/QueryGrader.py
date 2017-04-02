import re

import psycopg2
import sqlparse
from sqlparse.sql import Identifier, IdentifierList
from SqlLabApp.utils.DBUtils import get_db_connection

from SqlLabApp.utils.TestNameTableFormatter import test_name_table_format


# USAGE:
# 1) Queries must all be formatted using format_select_query
# 2) A query is 1 Select Query. There can be no create queries etc

def execute_formatted_query(fq):
    result = sqlparse.parse(sqlparse.format(fq, reindent=True, keyword_case='upper'))[0]

    if is_select_query(result):
        try:
            conn = get_db_connection()
            toRet = ""
            with conn.cursor() as cursor:
                cursor.execute(fq)
                r = cursor.fetchmany(10)
                for tuple in r:
                    toRet += str(tuple) + '\n'

                return toRet

        except psycopg2.Error as e:
            return e.pgerror

        except ValueError as e:
            return e.args

        finally:
            conn.close()

    else:
        return "Only Select Queries are allowed"


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


def format_select_query(tid, query_str):
    formatted_query = query_str
    table_name_list = get_tbl_names_from_select_query(query_str)
    table_dict = table_name_to_formatted(tid, table_name_list)

    for key in table_dict.keys():
        if key in query_str:
            formatted_query = str(re.sub(r'\b{0}\b'.format(key), table_dict.get(key), formatted_query)).strip()

    return formatted_query


def is_select_query(sqlparsed_result):
    return sqlparsed_result.token_first().value == 'SELECT'


def get_tbl_names_from_select_query(query_str):
    result = sqlparse.parse(sqlparse.format(query_str, reindent=True, keyword_case='upper'))[0]

    table_name_list = []
    toReturn = []
    if is_select_query(result):
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
