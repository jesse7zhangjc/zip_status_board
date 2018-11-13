"""
Run the Server
"""

# coding=utf-8
import tornado.ioloop
import tornado.options
import tornado.httpserver
from tornado.options import define, options

from db_config.set_up_env import set_up_mysql_db
from application import APPLICATION
from methods.host_ip import HOST_IP

define("port", default=8000, help="run on the given port", type=int)

def main():
    """
    Run the Server
    """
    print 'Setting up MySQL DB...'
    set_up_mysql_db()

    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(APPLICATION)
    http_server.listen(options.port)

    print "Server is running at http://%s:%s" % (HOST_IP, options.port)
    print "Quit the server with Ctrl+C"

    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
