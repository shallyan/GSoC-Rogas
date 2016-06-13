#coding = utf-8

import tornado.web
from handler import MainHandler, QueryHandler
import os

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r'/', MainHandler),
                    (r'/query', QueryHandler)]

        settings = {'template_path': os.path.join(os.path.dirname(__file__), '../template'),
                    'static_path': os.path.join(os.path.dirname(__file__), '../static'),
                    'autoreload': True,
                    'debug': True
                   }

        tornado.web.Application.__init__(self, handlers, **settings)
