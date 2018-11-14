"""
BaseHandler with headers
"""

import os
import binascii
import tornado.web


class BaseHandler(tornado.web.RequestHandler):
    """
    Base handler with authentication
    """

    def __init__(self, application, request, **kwargs):
        super(BaseHandler, self).__init__(application, request, **kwargs)

    def set_default_headers(self):
        """set headers
        """
        self.set_header("Access-Control-Allow-Origin", "http://localhost:3000")
        self.set_header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT, OPTIONS')
        self.set_header('Access-Control-Allow-Credentials', 'true')
        self.set_header('Content-Type', 'application/json')

    def options(self):
        """
        OPTION Method for CROS
        """
        self.set_status(200)
