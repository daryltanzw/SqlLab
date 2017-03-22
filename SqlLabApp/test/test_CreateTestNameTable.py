from unittest import TestCase
from SqlLabApp.utils.CreateTestNameTable import create_test_name_table
from SqlLabApp.utils.DBUtils import get_db_connection


class CreateTestNameTable(TestCase):

    def test_valid_create_test_name_table(self):
        q_a_file_lines = [
            "Select all females, with score higher than 50\tselect * from students where gender = 'F' and grade "
            "> 50;\t5",
            'q2\ta2\t4', 'q3\ta3\t3']

        connection = get_db_connection()
        cursor = connection.cursor()
        tbl_name = "Midterm1"

        try:
            create_test_name_table(cursor, tbl_name, q_a_file_lines)
            connection.close()
        except ValueError as err:
            self.fail(err)

    def test_invalid_create_test_name_table(self):
        raised = False
        q_a_file_lines = [
            "Select all females, with score higher than 50\tselect * from students where gender = 'F' and grade "
            "> 50;\t5",
            'q2\t4', 'q3\ta3\t3']

        connection = get_db_connection()
        cursor = connection.cursor()
        tbl_name = "Midterm1"

        try:
            create_test_name_table(cursor, tbl_name, q_a_file_lines)
            connection.close()
        except:
            connection.close()
            raised = True

        self.assertTrue(raised)