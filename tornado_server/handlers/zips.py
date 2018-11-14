"""Handle Zips Status Request
"""
from json import dumps
from concurrent.futures import ThreadPoolExecutor
from tornado import gen
from tornado.web import asynchronous
from tornado.concurrent import run_on_executor
from handlers import BaseHandler
from methods.crud_util import get_query_result

class ZipsHandler(BaseHandler):
    """List All Zips API
    """
    executor = ThreadPoolExecutor(4)

    @asynchronous
    @gen.coroutine
    def get(self):
        """
        List all zips status
        """
        rows = yield self.get_all_zip_status()
        rows_json = dumps(rows)
        self.write(rows_json)
        self.finish()

    @run_on_executor
    def get_all_zip_status(self):
        """List all zips and health status
        """

        #Check if there is remaining task, blocking task remaining, overall health status
        query = """
            SELECT
                z.id AS zip_id,
                z.name AS zip_name,
                IFNULL(task.task_done, 1) AS task_done,
                IFNULL(block.non_blocking, 1) AS non_blocking,
                IFNULL(task.task_done, 1) + IFNULL(block.non_blocking, 1) AS health
            FROM
                zip_list AS z
            LEFT JOIN
                (
                    SELECT
                        zip_id,
                        MIN(resolved) AS task_done
                    FROM
                        maintenance_task
                    GROUP BY
                        zip_id
                ) AS task
            ON
                z.id = task.zip_id
            LEFT JOIN
                (
                    SELECT
                        t.zip_id AS zip_id,
                        t.resolved AS resolved,
                        MIN(p.non_blocking) AS non_blocking
                    FROM
                        maintenance_task AS t
                    LEFT JOIN
                        problem_list AS p
                    ON
                        t.problem_id = p.id
                    WHERE t.resolved = 0
                    GROUP BY
                        t.zip_id
                ) AS block
            ON
                z.id = block.zip_id
            ORDER BY
                z.id
        """

        rows = get_query_result(query)
        return rows
