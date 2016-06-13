#coding = utf-8

from tornado import web
import config
from rogas import queryConsole

class BaseHandler(web.RequestHandler):
    """ base of handlers
    """
    pass

class MainHandler(BaseHandler):
    def get(self):
        self.render(config.MAIN_HTML)

class QueryHandler(BaseHandler):
    def post(self):
        query = self.get_argument('query')
        tab_index = self.get_argument('tab_index')

        queryResult = queryConsole.start(query)
        actResult = {'tab_index': tab_index, 'result': queryResult.asDict()}
        self.write(actResult)
