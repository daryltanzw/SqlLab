import re
import sqlparse
from TestNameTableFormatter import test_name_table_format


def append_to_relations(tid, query_line_list):
    ret = []
    query = '\n'.join(query_line_list)
    result_list = sqlparse.parse(sqlparse.format(query, reindent=True, keyword_case='upper'))
    table_dict = {}

    for result in result_list:
        if result.get_type() == 'CREATE':
            tbl_name = result.get_name()
            table_dict[tbl_name] = str(test_name_table_format(tid, tbl_name))

    for line in query_line_list:
        for key in table_dict.keys():
            if key in line:
                line = re.sub(r'\b{0}\b'.format(key), table_dict.get(key), line)

        ret.append(str(line))

    return ret
