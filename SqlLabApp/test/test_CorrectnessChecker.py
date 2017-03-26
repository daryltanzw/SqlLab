from autofixture import AutoFixture
from django.test import TestCase
from django_fake_model import models as m
from django.db import models
from SqlLabApp.utils.DBUtils import get_db_connection

from SqlLabApp.utils.CorrectnessChecker import CorrectnessChecker


class CorrectnessCheckerTest(TestCase):

    @classmethod
    def setUpClass(cls):
        connection = get_db_connection()
        statements = []
        with open('SqlLabApp/test/file/CorrectnessCheckerData.sql', 'r') as script:
            for statement in script:
                connection.cursor().execute(statement)
        connection.commit()

    def testSelectEquals(self):
        query1 = "SELECT i_name from item"
        query2 = query1
        correctnessChecker = CorrectnessChecker()
        result = correctnessChecker.compare(query1, query2)
        self.assertEqual(result, 0)

    def testSelectNotEquals(self):
        query1 = "SELECT i_name from item where i_id=1"
        query2 = "SELECT i_name from item where i_id=3"
        correctnessChecker = CorrectnessChecker()
        result = correctnessChecker.compare(query1, query2)
        self.assertEqual(result, 1)

    def testSelectEqualsJoinThreeTables(self):
        query1 = "SELECT i_name, s_qty from item i, stock s, warehouse w where i.i_id = s.i_id and w.w_id = s.w_id and w.w_id = 1"
        query2 = "SELECT i_name, s_qty from item i natural join stock s natural join warehouse w where w.w_id = 1"
        correctnessChecker = CorrectnessChecker()
        result = correctnessChecker.compare(query1, query2)
        self.assertEqual(result, 0)

    @classmethod
    def tearDownClass(cls):
        connection = get_db_connection()
        connection.cursor().execute("""DROP TABLE stock""")
        connection.cursor().execute("""DROP TABLE item""")
        connection.cursor().execute("""DROP TABLE warehouse""")
        connection.commit()

