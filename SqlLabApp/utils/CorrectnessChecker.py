# checks if teacher's query output = student's query output
from SqlLabApp.utils.DBUtils import get_db_connection


class CorrectnessChecker():

    def compare(self, query1, query2):
        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                query = "(" + query1 + " EXCEPT " + query2 + ")" + " UNION ALL " + "(" + query2 + " EXCEPT " + query1 + ")"
                cursor.execute(query)

                if cursor.rowcount == 0:
                    return 0

                # print differences
                else:
                    # rows = cursor.fetchall()
                    # print "\nRows: \n"
                    # for row in rows:
                    # print "   ", row[0]
                    return 1

        except ValueError as err:
            connection.close()
            raise err
