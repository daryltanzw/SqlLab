def test_name_table_format(tid, tbl_name):
    return str("tid" + str(tid) + "_" + tbl_name.replace("-", "").replace(" ", ""))


def student_attempt_table_format(tid, student_email, attempt_no):
    return str("tid" + str(tid) + "_" + str(student_email).replace("@", "").replace(".", "") + "_" + str(attempt_no))
