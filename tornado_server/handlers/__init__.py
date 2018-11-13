"""
init with a Base Handler with authoriazaiton check
"""

import os
import binascii
import tornado.web
from methods.host_ip import HOST_IP


class BaseHandler(tornado.web.RequestHandler):
    """
    Base handler with authentication
    """

    def __init__(self, application, request, **kwargs):
        super(BaseHandler, self).__init__(application, request, **kwargs)

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "http://%s:3000" % HOST_IP)
        self.set_header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT, OPTIONS')
        self.set_header('Access-Control-Allow-Credentials', 'true')

    def options(self):
        """
        OPTION Method for CROS
        """
        self.set_status(200)
        # self.finish()
