"""Handle Zips Status Request
"""
from json import dumps
from concurrent.futures import ThreadPoolExecutor
from tornado import gen
from tornado.concurrent import run_on_executor
from handlers import BaseHandler
from methods.crud_util import get_query_result

class ProblemsHandler(BaseHandler):
    """List All Zips API
    """
    executor = ThreadPoolExecutor(4)

    @gen.coroutine
    def get(self):
        """
        List all zips status
        """
        rows = yield self.get_all_problems()
        rows_json = dumps(rows)
        self.write(rows_json)
        self.finish()

    @run_on_executor
    def get_all_problems(self):
        """List all zips and health status
        """

        #Check if there is remaining task, blocking task remaining, overall health status
        query = """
            SELECT
                *
            FROM
                problem_list
            ORDER BY
                id
        """

        rows = get_query_result(query)
        return rows
