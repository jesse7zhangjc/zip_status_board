"""
Application
"""
import tornado.web
from url import URL


APPLICATION = tornado.web.Application(
    handlers=URL,
    )
