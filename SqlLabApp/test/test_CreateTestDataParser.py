from unittest import TestCase

from SqlLabApp.utils.CreateTestDataParser import append_to_relations


class CreateTestDataParser_Test(TestCase):
    def test_append_to_relations(self):
        tid = "1"

        with open("./file/TestData1.sql") as f:
            actual = f.read().splitlines()

        with open(
                "./file/ExpectedTestData1.sql") as fe:
            expected = fe.read().splitlines()

        result = append_to_relations(tid, actual)

        self.assertEqual(expected, result )

    def test_append_to_relations_2(self):
        tid = 5
        with open("./file/QueryGraderDatabase.sql") as f:
            actual = f.read().splitlines()

        with open("./file/ExpectedQueryGraderDatabase.sql") as fe:
            expected = fe.read().splitlines()

        result = append_to_relations(tid, actual)

        self.assertEqual( expected, result)