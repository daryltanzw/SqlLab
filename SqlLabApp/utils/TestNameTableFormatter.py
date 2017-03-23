
def test_name_table_format(tid, tbl_name):
    return str("tid" + str(tid) + "_" + tbl_name.replace("-", "").replace(" ", ""))
