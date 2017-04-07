import re

import psycopg2
import sqlparse
import sys
from sqlparse.tokens import Punctuation, Name

from SqlLabApp.models import QuestionDataUsedByTest
from SqlLabApp.utils.DBUtils import get_db_connection
from SqlLabApp.utils.TestNameTableFormatter import test_name_table_format


# USAGE:
# 1) Queries must all be formatted using format_select_query
# 2) A query is 1 Select Query. There can be no create queries etc

def is_query_against_visible(fq):
    try:
        pattern = re.compile('tid[1-9]+_')
        match = re.search(pattern, fq)
        if match:
            s = str(match.group(0))
            tid = re.search(r'\d+', s).group()
            invisible_tbl_list = QuestionDataUsedByTest.objects.filter(tid_id=tid, student_visibility=False).values(
                'data_tbl_name')
            for t in invisible_tbl_list:
                table_name = t['data_tbl_name']
                if test_name_table_format(tid, table_name) in fq:
                    return False

        return True
    except:
        return True


def execute_formatted_query(fq):
    if not is_query_against_visible(fq):
        return "Table is not Queryable"

    result = sqlparse.parse(sqlparse.format(fq, reindent=True, keyword_case='upper'))[0]

    if is_select_query(result):
        try:
            conn = get_db_connection()
            toRet = ""
            with conn.cursor() as cursor:
                cursor.execute(fq)
                r = cursor.fetchmany(5)
                for tuple in r:
                    toRet += str(tuple) + '\n'

                return toRet

        except psycopg2.Error as e:
            error = e.pgerror
            pattern = re.compile('tid[1-9]+_')
            match = re.search(pattern, error)
            if match:
                s = str(match.group(0))
                return error.replace(s, "")
            return error

        except ValueError as e:
            return e.args.replace("tid", "")

        finally:
            conn.close()

    else:
        return "Only Select Queries are allowed"


def is_select_query(sqlparsed_result):
    return sqlparsed_result.token_first().value == 'SELECT'

# Only grades 1 set of formatted student_query and teacher_query
def grade_formatted_query(student_query, teacher_query, mark):
    default_mark = 0

    try:
        conn = get_db_connection()
        fq1 = student_query.replace(";", "")
        fq2 = teacher_query.replace(";", "")

        with conn.cursor() as cursor:
            query = "( %s Except All %s) UNION ALL (%s EXCEPT All %s)" % (fq1, fq2, fq2, fq1)
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


def get_tbl_names_from_select_query(query_str):
    result = sqlparse.parse(sqlparse.format(query_str, reindent=True, keyword_case='upper'))[0]
    token_ls = process_and_flatten_token_list(result.tokens)
    tbl_names = []
    from_seen = False
    for i in range(0, len(token_ls)):
        token = token_ls[i]
        if token.is_keyword:
            if token.value == 'FROM':
                from_seen = True
                tbl_names.append(str(token_ls[i + 1].value))
            else:
                from_seen = False

        if from_seen and token.value == ",":
            tbl_names.append(str(token_ls[i + 1].value))
    return tbl_names


def process_and_flatten_token_list(tokens):
    res_unprocessed = []
    for token in tokens:
        if token.is_group:
            generator = token.flatten()
            for value in generator:
                res_unprocessed.append(value)
        else:

            res_unprocessed.append(token)

    res = []
    for token in res_unprocessed:
        if token.is_keyword or token.ttype == Punctuation or token.ttype == Name:
            res.append(token)

    return res


def table_name_to_formatted(tid, table_name_list):
    table_dict = {}
    for name in table_name_list:
        if not name in table_dict.keys():
            table_dict[name] = str(test_name_table_format(tid, name))

    return table_dict


# Method formats with hidden tables and grade multiple queries
def grade_query(tid, s_query, t_query, mark):
    s_used_tables_dict = table_name_to_formatted(tid, get_tbl_names_from_select_query(s_query))
    t_used_tables_dict = table_name_to_formatted(tid, get_tbl_names_from_select_query(t_query))

    if len(s_used_tables_dict) != len(
            t_used_tables_dict) or s_used_tables_dict.viewkeys() != t_used_tables_dict.viewkeys():
        return 0

    all_tables = []
    min_count = sys.maxint
    # Same set of tables are used by both queries
    for tbl_name in s_used_tables_dict:
        list_of_tbls = QuestionDataUsedByTest.objects.filter(tid_id=tid, data_tbl_name__icontains=tbl_name).values_list(
            'data_tbl_name', flat=True)
        t = TableToInvisibleContainer(tbl_name, list_of_tbls)
        all_tables.append(t)
        min_count = min(len(list_of_tbls), min_count)

    query_dict_ls = []
    # Set up a list of Query_dictionaries {item: "tid4_item1"} etc for regex replacement
    for i in range(0, min_count):
        query_dict = {}
        for table_container in all_tables:
            query_dict[table_container.tblname] = test_name_table_format(tid, table_container.tbl_list[i])

        query_dict_ls.append(query_dict)

    print "+++++++++++++++++++"
    print "Query dictionaries: "
    print query_dict_ls
    # mark each query dictionary
    for query_dict in query_dict_ls:
        i_student_query = change_tbl_names(query_dict, s_query)
        print "++++++++++ student query:" + str(i_student_query)
        i_teacher_query = change_tbl_names(query_dict, t_query)
        print "++++++++++ teacher query:" + str(i_teacher_query)
        marks_received = grade_formatted_query(i_student_query, i_teacher_query, mark)
        if marks_received == 0:
            return marks_received

    return mark


# Given a dictionary of {"from_tbl_name":"to_tbl_name",}, return a formatted query
def change_tbl_names(from_to_dict, query_str):
    formatted_query = query_str
    for key in from_to_dict.keys():
        if key in query_str:
            formatted_query = str(re.sub(r'\b{0}\b'.format(key), from_to_dict.get(key), formatted_query)).strip()

    return formatted_query


# Maps tbl name to list of all hidden tbl names including the tbl name itself
class TableToInvisibleContainer:
    def __init__(self, tbl_name, tbl_list):
        self.tblname = tbl_name
        self.tbl_list = tbl_list
