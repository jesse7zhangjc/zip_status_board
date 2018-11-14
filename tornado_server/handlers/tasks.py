"""Handle Image Request
"""
from json import dumps, loads
from concurrent.futures import ThreadPoolExecutor
from tornado import gen
from tornado.web import asynchronous
from tornado.concurrent import run_on_executor
from handlers import BaseHandler
from methods.crud_util import get_query_result, execute_query

class TasksHandler(BaseHandler):
    """List tasks for a zip or zips
    """
    executor = ThreadPoolExecutor(4)

    @asynchronous
    @gen.coroutine
    def get(self):
        """
        List all zips status
        """
        rows = yield self.get_all_tasks()
        rows_json = dumps(rows)
        self.write(rows_json)
        self.finish()

    @asynchronous
    @gen.coroutine
    def post(self):
        """Log new tasks
        """
        body = loads(self.request.body)
        zip_id = body['zip_id']
        prob_ids = body['prob_ids']
        print zip_id
        print prob_ids
        result = yield self.add_new_tasks(zip_id, prob_ids)
        if result:
            ret_json = dumps({'message': 'success!'})
            self.write(ret_json)
            self.set_status(200)
            self.finish()
        else:
            ret_json = dumps({'message': 'failure!'})
            self.write(ret_json)
            self.set_status(400)
            self.finish()

    @asynchronous
    @gen.coroutine
    def put(self):
        """API for implement a task
        """
        body = loads(self.request.body)
        task_ids = body['task_ids']
        resolve = body['resolve']
        result = yield self.implement_tasks(task_ids=task_ids, resolve_value=resolve)
        if result >= 0:
            ret_json = dumps({'message': 'success!'})
            self.write(ret_json)
            self.set_status(200)
            self.finish()
        else:
            ret_json = dumps({'message': 'task not found!'})
            self.write(ret_json)
            self.set_status(404)
            self.finish()

    @run_on_executor
    def get_all_tasks(self):
        """List tasks for all zips
        """

        #Check if there is remaining task, blocking task remaining, overall health status
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
            ORDER BY
                t.resolved ASC,
                p.non_blocking ASC,
                t.zip_id ASC
        """

        rows = get_query_result(query)
        return rows

    

    @run_on_executor
    def add_new_tasks(self, zip_id, prob_ids):
        """Log new maintenance task
        """
        values = ['(%s, %s, 0)' % (zip_id, prob_id) for prob_id in prob_ids]
        value_str = ', '.join(values)
        query = """
            INSERT INTO
                maintenance_task (zip_id, problem_id, resolved)
            VALUES
                %s
        """ % value_str
        result = execute_query(query)
        return result

    # @run_on_executor
    # def implement_a_task(self, task_id, resolve_value):
    #     """Mark a task as resolved
    #     """

    #     query = """
    #         UPDATE maintenance_task
    #         SET resolved = %(resolve_value)s
    #         WHERE id = %(task_id)s
    #     """

    #     result = execute_query(query, task_id=task_id, resolve_value=resolve_value)
    #     return result

    @run_on_executor
    def implement_tasks(self, task_ids, resolve_value):
        """Mark a task as resolved
        """

        query = """
            UPDATE maintenance_task
            SET resolved = %(resolve_value)s
            WHERE id in %(task_ids)s
        """

        result = execute_query(query, task_ids=task_ids, resolve_value=resolve_value)
        return result
