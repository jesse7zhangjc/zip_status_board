"""Handle one Zip Status Request
"""
from json import dumps
from concurrent.futures import ThreadPoolExecutor
from tornado import gen
from tornado.web import asynchronous
from tornado.concurrent import run_on_executor
from handlers import BaseHandler
from methods.crud_util import get_query_result

class ZipHandler(BaseHandler):
    """List All Zips API
    """
    executor = ThreadPoolExecutor(4)

    @asynchronous
    @gen.coroutine
    def get(self, zip_id):
        """
        List all zips status
        """
        zip_obj = yield self.get_zip_obj(zip_id)
        if zip_obj:
            rows_json = dumps(zip_obj)
            self.write(rows_json)
            self.finish()
        else:
            self.set_status(404)
            self.write(dumps({ 'error': 'Zip Not Found' }))
            self.finish()

    @run_on_executor
    def get_zip_obj(self, zip_id):
        """Get zip object
        """
        status = self.get_zip_current_status(zip_id)
        if status:
            zip_obj = {'status': status}
            task_history = self.get_zip_task_history(zip_id)
            zip_obj['task_history'] = task_history
            return zip_obj
        return {}


    def get_zip_current_status(self, zip_id):
        """List all zips and health status
        """

        #Check if there is remaining task, blocking task remaining, overall health status
        query = """
            SELECT
                z.id AS zip_id,
                z.name AS zip_name,
                IFNULL(task.task_done, 1) AS health,
                IFNULL(task.task_remain, 0) AS task_remain,
                IFNULL(block.task_block, 0) AS task_block,
                IFNULL(block.ok_to_fly, 1) AS ok_to_fly,
                IFNULL(task.task_done, 1) + IFNULL(block.ok_to_fly, 1) AS status
            FROM
                zip_list AS z
            LEFT JOIN
                (
                    SELECT
                        zip_id,
                        MIN(resolved) AS task_done,
                        COUNT(*) AS task_remain
                    FROM
                        maintenance_task
                    WHERE
                        resolved = 0
                        AND zip_id = %(zip_id)s
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
                        COUNT(*) AS task_block,
                        IF(COUNT(*) = 0, 1, 0) AS ok_to_fly
                    FROM
                        maintenance_task AS t
                    LEFT JOIN
                        problem_list AS p
                    ON
                        t.problem_id = p.id
                    WHERE
                        t.resolved = 0
                        AND zip_id = %(zip_id)s
                        AND p.non_blocking = 0
                    GROUP BY
                        t.zip_id
                ) AS block
            ON
                z.id = block.zip_id
            WHERE
                z.id = %(zip_id)s
            ORDER BY
                z.id;
        """

        rows = get_query_result(query, zip_id=zip_id)
        if rows:
            return rows[0]
        return {}

    def get_zip_task_history(self, zip_id):
        """List tasks for a zip
        """
        query = """
            SELECT
                t.id AS task_id,
                t.zip_id AS zip_id,
                z.name AS zip_name,
                t.problem_id AS problem_id,
                p.name AS problem_name,
                t.resolved AS resolved,
                p.non_blocking AS non_blocking

            FROM
                maintenance_task AS t
            LEFT JOIN
                problem_list AS p
            ON
                t.problem_id = p.id
            LEFT JOIN
                zip_list AS z
            ON
                t.zip_id = z.id
            WHERE
                t.zip_id = %(zip_id)s
            ORDER BY
                t.resolved ASC,
                p.non_blocking ASC,
                t.zip_id ASC
        """
        rows = get_query_result(query, zip_id=zip_id)
        return rows
