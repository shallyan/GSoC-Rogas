'''
The resultManager is to manage the query results

@author: Yan Xiao
'''

import config

class TableResult(object):
    def __init__(self, column_list=None, row_content=None, is_begin=1, is_end=1, query_id=0):
        self.column_list = column_list
        self.row_content = row_content 
        self.is_end = is_end
        self.is_begin = is_begin
        self.query_id = query_id

    def setQueryId(self, query_id):
        self.query_id = query_id

    def asDict(self):
        return {'column_list': self.column_list, 'row_content': self.row_content, 'is_begin': self.is_begin, 'is_end': self.is_end, 'query_id': self.query_id}
    
    def asReturnResult(self):
        return {'table': self.asDict()}

class GraphResult(object):
    def __init__(self, graph_operator, graph_type, graph_name):
        self.setGraphOperator(graph_operator)
        self.setGraphType(graph_type)
        self.setGraphName(graph_name)

    def setGraphType(self, graph_type):
        if graph_type not in ['digraph', 'ungraph']:
            raise TypeError('graph type must be digraph or ungraph') 
        self.graph_type = graph_type

    def setGraphOperator(self, graph_operator):
        if graph_operator not in ['rank', 'cluster', 'path']:
            raise TypeError('graph operator must be rank, cluster or path') 
        self.graph_operator = graph_operator
    
    def setGraphName(self, graph_name):
        self.graph_name = graph_name

    def readGraphFile(self):
        matGraphFile = os.environ['HOME'] + "/RG_Mat_Graph/" + self.graph_name
        with open(matGraphFile) as f:
            pass

    def asDict(self):
        return {'name': self.graph_name, 'operator': self.graph_operator, 'graph_type': self.graph_type}
    
    def asReturnResult(self):
        return {'graph': self.asDict()}

class TableGraphResult(object):
    def __init__(self, table_result, graph_result):
        self.table_result = table_result
        self.graph_result = graph_result
    
    def asReturnResult(self):
        return {'table': self.table_result.asDict(), 'graph': self.graph_result.asDict()}

class QueryResult(object):
    def __init__(self, result_type='string', result_content='None'):
        #type: string, table, table+graph
        self.setType(result_type)
        self.setContent(result_content)

    def setType(self, result_type):
        if result_type not in ['string', 'table', 'table_graph']:
            raise TypeError('Query result type must be string, table or table_graph') 
        self.result_type = result_type
    
    def setContent(self, result_content):
        self.result_content = result_content
    
    def asReturnResult(self):
        content_val = self.result_content if self.result_type == 'string' else self.result_content.asReturnResult()
        return {'type': self.result_type, 'content': content_val}

class ResultManager(object):
    def __init__(self):
        self.current_id = 0
        self.cursor_dict = {}

    def _extractTableResult(self, cursor, is_next, max_number):
        start_index = cursor.rownumber 
        #previous page
        if is_next == 0:
            #if current in last page
            if cursor.rownumber == cursor.rowcount:
                start_index = cursor.rownumber - max_number - cursor.rowcount % max_number 
            else:
                start_index = cursor.rownumber - 2*max_number
        start_index = 0 if start_index < 0 else start_index

        if start_index >= cursor.rowcount:
            return 1, TableResult([], [])

        column_list = [desc[0] for desc in cursor.description]
        rows_content = []

        cursor.scroll(start_index, mode='absolute')
        rows = cursor.fetchmany(max_number)
        for each_row in rows:
            one_row_content = [str(each_col) for each_col in each_row]
            rows_content.append(one_row_content)

        is_end = 1 if cursor.rownumber == cursor.rowcount else 0
        is_begin = 1 if start_index == 0 else 0

        return is_end, TableResult(column_list, rows_content, is_begin, is_end)

    def extractTableResultFromCursor(self, cursor):
        is_end, table_result = self._extractTableResult(cursor, 0, config.PAGE_MAX_NUM)
        
        if is_end == 0:
            table_result.setQueryId(self.current_id)
            self.addCursor(cursor) 
        
        return table_result

    def addCursor(self, cursor):
        self.cursor_dict[self.current_id] = cursor
        self.current_id += 1
    
    def removeCursor(self, id):
        self.cursor_dict.pop(id)

    def extractTableResultById(self, id, is_next):
        if id not in self.cursor_dict:
            return TableResult([], [])

        cursor = self.cursor_dict[id]
        _, table_result = self._extractTableResult(cursor, is_next, config.PAGE_MAX_NUM)
        table_result.setQueryId(id)

        return table_result

SingleResultManager = ResultManager()
