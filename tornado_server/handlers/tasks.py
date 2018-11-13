"""Handle Image Request
"""
from json import dumps
from concurrent.futures import ThreadPoolExecutor
from tornado import gen
from tornado.concurrent import run_on_executor
from handlers import BaseHandler
from methods.crud_util import get_query_result, execute_query

class TasksHandler(BaseHandler):
    """List tasks for a zip or zips
    """
    executor = ThreadPoolExecutor(4)

    @gen.coroutine
    def get(self):
        """
        List all zips status
        """
        zip_id = self.get_arguments('zip_id')
        if zip_id:
            rows = yield self.tasks_for_a_zip(zip_id)
        else:
            rows = yield self.tasks_for_zips()
        rows_json = dumps(rows)
        self.write(rows_json)
        self.finish()

    @gen.coroutine
    def post(self):
        """Log new tasks
        """
        zip_id = self.get_arguments('zip_id')
        prob_id = self.get_arguments('prob_id')
        result = yield self.add_new_task(zip_id, prob_id)
        if result:
            ret_json = dumps({'message': 'success!'})
            self.write(ret_json)
            self.set_status(200)
        else:
            ret_json = dumps({'message': 'failure!'})
            self.write(ret_json)
            self.set_status(400)

    @gen.coroutine
    def put(self):
        """API for implement a task
        """
        task_id = self.get_arguments('task_id')

        result = yield self.implement_a_task(task_id)
        print result
        if result >= 0:
            ret_json = dumps({'message': 'success!'})
            self.write(ret_json)
            self.set_status(200)
        else:
            ret_json = dumps({'message': 'task not found!'})
            self.write(ret_json)
            self.set_status(404)

    @run_on_executor
    def tasks_for_zips(self):
        """List tasks for all zips
        """

        #Check if there is remaining task, blocking task remaining, overall health status
        query = """
            SELECT
                t.zip_id AS zip_id,
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
            ORDER BY
                t.resolved ASC,
                p.non_blocking ASC,
                t.zip_id ASC
        """

        rows = get_query_result(query)
        return rows

    @run_on_executor
    def tasks_for_a_zip(self, zip_id):
        """List tasks for a zip
        """
        query = """
            SELECT
                t.zip_id AS zip_id,
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
            WHERE zip_id = %(zip_id)s
            ORDER BY
                t.resolved ASC,
                p.non_blocking ASC,
                t.zip_id ASC
        """
        rows = get_query_result(query, zip_id=zip_id)
        return rows

    @run_on_executor
    def add_new_task(self, zip_id, prob_id):
        """Log new maintenance task
        """
        query = """
            INSERT INTO
                maintenance_task (zip_id, problem_id, resolved)
            VALUES (%(zip_id)s, %(prob_id)s, 0)
        """
        result = execute_query(query, zip_id=zip_id, prob_id=prob_id)
        return result

    @run_on_executor
    def implement_a_task(self, task_id):
        """Mark a task as resolved
        """

        query = """
            UPDATE maintenance_task
            SET resolved = 1
            WHERE id = %(task_id)s
        """

        result = execute_query(query, task_id=task_id)
        return result

    @run_on_executor
    def implement_tasks(self, task_ids):
        """Mark a task as resolved
        """

        query = """
            UPDATE maintenance_task
            SET resolved = 1
            WHERE id = %(task_id)s
        """

        result = execute_query(query, task_ids=task_ids)
        return result
