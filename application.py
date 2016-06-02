#coding = utf-8

import tornado.web
from handler import MainHandler
import os

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r'/', MainHandler),
                    (r'/index.html', MainHandler)]

        settings = {'template_path': os.path.join(os.path.dirname(__file__), 'template'),
                    'static_path': os.path.join(os.path.dirname(__file__), 'static'),
                    'autoreload': True
                   }

        tornado.web.Application.__init__(self, handlers, **settings)
