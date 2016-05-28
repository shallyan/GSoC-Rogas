#coding = utf-8

from tornado import web
import config

class BaseHandler(web.RequestHandler):
    """ base of handlers
    """
    pass

class MainHandler(BaseHandler):
    def get(self):
        self.render(config.MAIN_HTML)
