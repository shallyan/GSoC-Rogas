#coding = utf-8

import tornado.web
from handler import MainHandler, QueryHandler, LoadResultHandler, ConfigHandler
import os
from rogas import queryConsole

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r'/', MainHandler),
                    (r'/load_result', LoadResultHandler),
                    (r'/query', QueryHandler),
                    (r'/config', ConfigHandler)]

        settings = {'template_path': os.path.join(os.path.dirname(__file__), '../template'),
                    'static_path': os.path.join(os.path.dirname(__file__), '../static'),
                    'autoreload': True,
                    'debug': True
                   }

        tornado.web.Application.__init__(self, handlers, **settings)

        queryConsole.prepare()
