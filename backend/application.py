#coding = utf-8

import tornado.web
from handler import MainHandler, QueryHandler, LoadResultHandler, ConfigHandler, RelationCoreInfoHandler, GraphicalViewInfoHandler
import os
from rogas import queryConsole

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r'/', MainHandler),
                    (r'/load_result', LoadResultHandler),
                    (r'/run_query', QueryHandler),
                    (r'/update_config', ConfigHandler),
                    (r'/get_relation_core_info', RelationCoreInfoHandler),
                    (r'/get_graphical_view_info', GraphicalViewInfoHandler)]

        settings = {'template_path': os.path.join(os.path.dirname(__file__), '../template'),
                    'static_path': os.path.join(os.path.dirname(__file__), '../static'),
                    'autoreload': True,
                    'debug': True
                   }

        tornado.web.Application.__init__(self, handlers, **settings)

        queryConsole.prepare()
