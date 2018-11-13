"""
url structure of apis
"""
from handlers.zip import ZipHandler
from handlers.zips import ZipsHandler
from handlers.tasks import TasksHandler
from handlers.problems import ProblemsHandler

URL = [
    (r'/zips', ZipsHandler),
    (r'/zips/(.+)', ZipHandler),
    (r'/tasks', TasksHandler),
    (r'/problems', ProblemsHandler),
]
