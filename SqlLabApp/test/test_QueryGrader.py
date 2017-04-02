from unittest import TestCase
import SqlLabApp.utils.QueryGrader as grader
from SqlLabApp.utils.DBUtils import get_db_connection


# WARNING: Will actually create and try to delete tables. Ensure deletion
class QueryGrader_Test(TestCase):
    @classmethod
    def setUpClass(cls):
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("""DROP TABLE if exists item CASCADE""")
            cursor.execute("""DROP TABLE if exists warehouse CASCADE""")
            cursor.execute("""DROP TABLE if exists stock CASCADE""")
            cursor.execute("""DROP TABLE if exists item1 CASCADE""")
            cursor.execute("""DROP TABLE if exists warehouse1 CASCADE""")
            cursor.execute(open("./file/QueryGraderDatabase.sql", "r").read())
            connection.commit()
            connection.close()

    @classmethod
    def tearDownClass(cls):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("""DROP TABLE if exists item CASCADE""")
        cursor.execute("""DROP TABLE if exists warehouse CASCADE""")
        cursor.execute("""DROP TABLE if exists stock CASCADE""")
        cursor.execute("""DROP TABLE if exists item1 CASCADE""")
        cursor.execute("""DROP TABLE if exists warehouse1 CASCADE""")
        connection.commit()
        connection.close()

    def test_format_query(self):
        tid = 5
        input = "select * from warehouse where w_country='Singapore';"
        expected = "select * from tid{0}_warehouse where w_country='Singapore';".format(tid)
        formatted_query = grader.format_select_query(tid, input)
        self.assertEqual(expected, formatted_query)

        tid = 4
        input = "select i.i_name from item i, stock s where i.i_id = s.i_id and s.s_qty > 400;"
        expected = "select i.i_name from tid{0}_item i, tid{0}_stock s where i.i_id = s.i_id and s.s_qty > 400;".format(
            tid)
        formatted_query = grader.format_select_query(tid, input)
        self.assertEqual(expected, formatted_query)

    def test_grade_formatted_query(self):
        fq1 = "select * from warehouse where w_country='Singapore';"
        fq2 = "select * from warehouse where w_country='Singapore';"
        self.assertEqual(3, grader.grade_formatted_query(fq1, fq2, 3))

        fq1 = "select * from warehouse where w_country='Singapore';"
        fq2 = "select * from warehouse where w_country='China';"
        self.assertEqual(0, grader.grade_formatted_query(fq1, fq2, 3))
