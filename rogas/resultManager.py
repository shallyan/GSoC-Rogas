'''
The resultManager is to manage the query results

@author: Yan Xiao
'''

import config
import queryConsole
import os
import random

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
        return {'column_list': self.column_list, 'row_content': self.row_content,
                'is_begin': self.is_begin, 'is_end': self.is_end, 
                'query_id': self.query_id}
    
    def asReturnResult(self):
        return {'table': self.asDict()}

class GraphResult(object):
    def __init__(self, graph_operator, graph_type, graph_name, graph_op_result_name):
        self.setGraphOperator(graph_operator)
        self.setGraphType(graph_type)
        self.setGraphName(graph_name)
        self.setGraphOpResultName(graph_op_result_name)

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

    def setGraphOpResultName(self, graph_op_result_name):
        self.graph_op_result_name = graph_op_result_name 
    
    def _generateRankGraphNodes(self, row_content):
        self.graph_nodes = []

        #VertexId, Value
        for row in row_content:
            node = {'id': str(row[0].strip()), 'size': float(row[1].strip()),'color': 0}
            self.graph_nodes.append(node)

        #keep max and min nodes
        max_num = config.RANK_NODE_MAX_NUM
        if len(self.graph_nodes) > max_num:
            self.graph_nodes = self.graph_nodes[:max_num/2] + self.graph_nodes[-max_num/2:]

    def _generateClusterGraphNodes(self, row_content):
        self.graph_nodes = []
        cluster_id2size = dict()
        cluster_id2nodes = dict()
        node_id2cluster_id = dict()
        node_id2score = dict()
        node_id_cluster_id2score_reatio = dict()
        all_nodes_num = 0

        #ClusterId, Size, Members
        for row in row_content:
            cluster_id = str(row[0].strip())
            cluster_size = float(row[1].strip())
            cluster_members = str(row[2].strip())
            node_ids = [node_id.strip() for node_id in cluster_members[1:-1].split(',')]
            all_nodes_num += cluster_size
            
            cluster_id2size[cluster_id] = cluster_size
            cluster_id2nodes[cluster_id] = node_ids
            for node_id in node_ids:
                node_id2cluster_id[node_id] = cluster_id 
                node_id2score[node_id] = 0
                if node_id not in node_id_cluster_id2score_reatio:
                    node_id_cluster_id2score_reatio[node_id] = dict()

        for node_id in node_id_cluster_id2score_reatio:
            for cluster_id in cluster_id2size:
                node_id_cluster_id2score_reatio[node_id][cluster_id] = 2.0
        
        need_scale_size = all_nodes_num > config.CLUSTER_NODE_MAX_NUM

        for edge in self.graph_edges:
            start_node = edge['source']
            end_node = edge['target']
            #two node in the same cluster
            source_cluster_id = node_id2cluster_id[start_node]
            target_cluster_id = node_id2cluster_id[end_node]

            #score each node if needed
            if source_cluster_id == target_cluster_id:
                if need_scale_size:
                    node_id2score[start_node] += 1.0
                    node_id2score[end_node] += 1.0
            else:
                edge['length'] = 400 + random.random()*100
                if need_scale_size:
                    node_id2score[start_node] += node_id_cluster_id2score_reatio[start_node][target_cluster_id]
                    node_id_cluster_id2score_reatio[start_node][target_cluster_id] *= 0.8

                    node_id2score[end_node] += node_id_cluster_id2score_reatio[end_node][source_cluster_id]
                    node_id_cluster_id2score_reatio[end_node][source_cluster_id] *= 0.8


        if need_scale_size:
            #calculate the size of each cluster
            for cluster_id, cluster_size in cluster_id2size.items():
                cluster_id2size[cluster_id] = max(cluster_size * config.CLUSTER_NODE_MAX_NUM * 1.0 / all_nodes_num, 5)

            #keep high score nodes
            for cluster_id, cluster_nodes in cluster_id2nodes.iteritems():
                score_node_id_pair_lst = [(node_id2score[node_id], node_id) for node_id in cluster_nodes]
                #sort node by score
                sorted_score_node_id_pair_lst = sorted(score_node_id_pair_lst)
                #get nodes
                max_nodes_num = min(len(score_node_id_pair_lst), cluster_id2size[cluster_id])
                for i in range(int(max_nodes_num)):
                    node_id = sorted_score_node_id_pair_lst[i][1]
                    node = {'id': node_id, 'size': 0.1, 'color': cluster_id}
                    self.graph_nodes.append(node)

        else:
            #keep all nodes 
            for cluster_id, cluster_nodes in cluster_id2nodes.iteritems():
                for node_id in cluster_nodes:
                    node = {'id': node_id, 'size': 0.05, 'color': cluster_id}
                    self.graph_nodes.append(node)

    def _generatePathGraphNodes(self, row_content):
        self._generateGraphNodes()

    def _generateGraphNodes(self):
        #To do
        self.graph_nodes = []
        node1 = {'id': '1', 'size': 0.5 ,'color': 0}
        node2 = {'id': '2', 'size': 0.5 ,'color': 0}
        self.graph_nodes.append(node1)
        self.graph_nodes.append(node2)

    def _generateGraphEdges(self, matGraphFile): 
        self.graph_edges = []

        with open(matGraphFile) as f:
            for line in f:
                edge_nodes = line.strip().split()
                edge = {'source': str(edge_nodes[0].strip()), 'target': str(edge_nodes[1].strip()),
                        'length': 100, 'width': 1, 'color': 1}
                self.graph_edges.append(edge)

    def _filterEdgesByNodes(self):
        all_nodes_id_set = set([node['id'] for node in self.graph_nodes])
        new_graph_edges = []

        for edge in self.graph_edges:
            if edge['source'] in all_nodes_id_set and edge['target'] in all_nodes_id_set:
                new_graph_edges.append(edge)

        self.graph_edges = new_graph_edges

    def generateGraph(self):
        #read graph edges from file
        matGraphFile = os.environ['HOME'] + "/RG_Mat_Graph/" + self.graph_name
        self._generateGraphEdges(matGraphFile)

        #read graph nodes 
        tableResult = queryConsole.readTable(self.graph_op_result_name)
        if self.graph_operator == 'rank':
            self._generateRankGraphNodes(tableResult.row_content)
        elif self.graph_operator == 'cluster':
            self._generateClusterGraphNodes(tableResult.row_content)
        elif self.graph_operator == 'path':
            self._generatePathGraphNodes(tableResult.row_content)
        else:
            self._generateGraphNodes()

        #filter edges by nodes
        self._filterEdgesByNodes()

    def asDict(self):
        return {'name': self.graph_name, 'operator': self.graph_operator, 
                'graph_type': self.graph_type, 'nodes': self.graph_nodes,
                'edges': self.graph_edges}
    
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

    def _extractTableResult(self, cursor, is_next, max_number, is_all=False):
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
        rows = cursor.fetchall() if is_all else cursor.fetchmany(max_number)
        for each_row in rows:
            one_row_content = [str(each_col) for each_col in each_row]
            rows_content.append(one_row_content)

        is_end = 1 if cursor.rownumber == cursor.rowcount else 0
        is_begin = 1 if start_index == 0 else 0

        return is_end, TableResult(column_list, rows_content, is_begin, is_end)

    def extractTableResultFromCursor(self, cursor, is_all=False):
        is_end, table_result = self._extractTableResult(cursor, 0, config.PAGE_MAX_NUM, is_all)
        
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
