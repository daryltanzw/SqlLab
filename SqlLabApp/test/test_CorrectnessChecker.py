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

    def testNestedInSelectEquals(self):
        query1 = "Select i.i_id, i.i_name, i.i_price from item i where i.i_id IN (Select s.i_id from stock s where s.w_id = 1) and i.i_id not in (Select s1.i_id from stock s1 where s1.w_id = 3) "
        query2 = "Select i.i_id, i.i_name, i.i_price from item i, stock s where i.i_id = s.i_id and s.w_id = 1 except Select i.i_id, i.i_name, i.i_price from item i, stock s where i.i_id = s.i_id and s.w_id = 3"
        correctnessChecker = CorrectnessChecker()
        result = correctnessChecker.compare(query1, query2)
        self.assertEqual(result, 0)

    def testSelectGroupBysEquals(self):
        query1 = "Select count(s.i_id), s.w_id from stock s group by s.w_id"
        query2 = "Select count(s.i_id), s.w_id from stock s group by s.w_id"
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

