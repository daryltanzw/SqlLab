import re
import sqlparse
from TestNameTableFormatter import test_name_table_format


def append_to_relations(tid, query_line_list):
    ret = []
    table_name_list = get_tbl_names(query_line_list)
    table_dict = table_name_to_formatted(tid, table_name_list)

    for line in query_line_list:
        for key in table_dict.keys():
            if key in line:
                line = re.sub(r'\b{0}\b'.format(key), table_dict.get(key), line)

        ret.append(str(line))

    return ret


def get_tbl_names(query_line_list):
    query = '\n'.join(query_line_list)
    result_list = sqlparse.parse(sqlparse.format(query, reindent=True, keyword_case='upper'))

    table_name_list = []

    for result in result_list:
        if result.get_type() == 'CREATE':
            tbl_name = result.get_name()
            table_name_list.append(tbl_name)

    return table_name_list


def table_name_to_formatted(tid, table_name_list):
    table_dict = {}
    for name in table_name_list:
        table_dict[name] = str(test_name_table_format(tid, name))

    return table_dict
