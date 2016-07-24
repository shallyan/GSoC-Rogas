'''
The resultManager is to manage the query results

@author: Yan Xiao
'''

import config
import queryConsole
import os
import random
import helper

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
    def __init__(self, graph_operator, graph_type, graph_name, graph_op_result_name, graph_condition):
        self.setGraphOperator(graph_operator)
        self.setGraphType(graph_type)
        self.setGraphName(graph_name)
        self.setGraphOpResultName(graph_op_result_name)
        self.setGraphCondition(graph_condition)

    def setGraphType(self, graph_type):
        if graph_type not in ['digraph', 'ungraph']:
            raise TypeError('graph type must be digraph or ungraph') 
        self.graph_type = graph_type

    def setGraphOperator(self, graph_operator):
        if graph_operator not in ['all', 'rank', 'cluster', 'path']:
            raise TypeError('graph operator must be all, rank, cluster or path') 
        self.graph_operator = graph_operator
    
    def setGraphName(self, graph_name):
        self.graph_name = graph_name

    def setGraphOpResultName(self, graph_op_result_name):
        self.graph_op_result_name = graph_op_result_name 
    
    def setGraphCondition(self, graph_condition):
        self.graph_condition = graph_condition 

    def _generateRankSelectNodes(self, row_content):
        node_size = {}
        min_value = 1.0
        max_value = 0.0

        #VertexId, Value
        for row in row_content:
            node_value = float(row[1].strip())
            node_size[str(row[0].strip())] = node_value           

            if node_value < min_value: 
                min_value = node_value
            if node_value > max_value:
                max_value = node_value

            if len(node_size) > config.RANK_NODE_MAX_NUM:
                break

        #scale node value for visualizaiion 
        for node_id, node_value in node_size.iteritems():
            node_value = config.NODE_MIN_SIZE + int((node_value - min_value) * (config.NODE_MAX_SIZE - config.NODE_MIN_SIZE) / (0.001 + max_value - min_value))
            node_size[node_id] = node_value
        
        return node_size

    def _generateClusterGraphNodes(self, row_content, keep_nodes):
        self.graph_nodes = []
        cluster_id2size = dict()
        cluster_id2nodes = dict()
        cluster_id2keep_nodes = dict()
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
            cluster_id2keep_nodes[cluster_id] = {} 

            for node_id in node_ids:
                node_id2cluster_id[node_id] = cluster_id 
                node_id2score[node_id] = 0
                if node_id not in node_id_cluster_id2score_reatio:
                    node_id_cluster_id2score_reatio[node_id] = dict()

        for node_id in node_id_cluster_id2score_reatio:
            for cluster_id in cluster_id2size:
                node_id_cluster_id2score_reatio[node_id][cluster_id] = 2.0
        
        for node_id, node_value in keep_nodes.iteritems():
            if node_id in node_id2cluster_id:
                cluster_id = node_id2cluster_id[node_id]
                cluster_id2keep_nodes[cluster_id][node_id] = node_value
            else:
                print 'data changes between graph creation and rank operation:', node_id
            

        need_scale_size = all_nodes_num > config.GRAPH_NODE_MAX_NUM

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
                edge['length'] = 700 + random.random()*100
                if need_scale_size:
                    node_id2score[start_node] += node_id_cluster_id2score_reatio[start_node][target_cluster_id]
                    node_id_cluster_id2score_reatio[start_node][target_cluster_id] *= 0.8

                    node_id2score[end_node] += node_id_cluster_id2score_reatio[end_node][source_cluster_id]
                    node_id_cluster_id2score_reatio[end_node][source_cluster_id] *= 0.8


        if need_scale_size:
            #calculate the size of each cluster
            for cluster_id, cluster_size in cluster_id2size.items():
                cluster_id2size[cluster_id] = max(cluster_size * config.GRAPH_NODE_MAX_NUM * 1.0 / all_nodes_num, 5)

            #keep high score nodes
            for cluster_id, cluster_nodes in cluster_id2nodes.iteritems():
                #get nodes num
                max_nodes_num = min(len(cluster_nodes), cluster_id2size[cluster_id])

                score_node_id_pair_lst = [(node_id2score[node_id], node_id) for node_id in cluster_nodes]
                #sort node by score
                sorted_score_node_id_pair_lst = sorted(score_node_id_pair_lst)

                #get  max_nodes_num from sorted_score_node_id_pair_lst and keep nodes
                #keep nodes first
                cluster_nodes_count = 0
                for node_id, node_value in cluster_id2keep_nodes[cluster_id].iteritems():
                    node = {'id': node_id, 'size': node_value, 'color': cluster_id, 'highlight': 1, 'opacity': 1.0}
                    self.graph_nodes.append(node)
                    cluster_nodes_count += 1

                for i in range(len(sorted_score_node_id_pair_lst)):
                    if cluster_nodes_count > max_nodes_num:
                        break

                    node_id = sorted_score_node_id_pair_lst[i][1]
                    if node_id not in cluster_id2keep_nodes[cluster_id]:
                        node = {'id': node_id, 'size': config.NODE_DEFAULT_SIZE, 'color': cluster_id, 'highlight': 0, 'opacity': 1.0}
                        self.graph_nodes.append(node)
                        cluster_nodes_count += 1

        else:
            #keep all nodes 
            for cluster_id, cluster_nodes in cluster_id2nodes.iteritems():
                for node_id in cluster_nodes:
                    node = {'id': node_id, 'size': config.NODE_DEFAULT_SIZE, 'color': cluster_id, 'highlight': 0, 'opacity': 1.0}
                    if node_id in keep_nodes:
                        node['size'] = keep_nodes[node_id]
                    self.graph_nodes.append(node)

    def _formatPathEdge(self, node_one, node_two):
        if self.graph_type == "digraph":
            return (node_one, node_two)

        if node_one < node_two:
            return (node_one, node_two)
        return (node_two, node_one)

    def _generatePathGraphNodes(self, row_content):
        self.graph_nodes = []

        path_nodes_set = set()
        path_edges2path_ids = dict()

        #find nodes in the path
        for index, row in enumerate(row_content):
            if index >= config.PATH_MAX_NUM:
                break

            #PathId, Length, Paths 
            path_id = int(row[0].strip())
            path_nodes = str(row[2].strip())
            path_node_ids = [node_id.strip() for node_id in path_nodes[1:-1].split(',')]
            for node_id_index, node_id in enumerate(path_node_ids):
                if node_id_index > 0:
                    one_path_edge = self._formatPathEdge(path_node_ids[node_id_index-1], node_id)
                    if one_path_edge not in path_edges2path_ids:
                        path_edges2path_ids[one_path_edge] = set()
                    path_edges2path_ids[one_path_edge].add(2**path_id)
                
                path_nodes_set.add(node_id)

        #find nodes around the path
        around_path_nodes_set = set()
        for edge in self.graph_edges:
            edge['opacity'] = config.UNHIGHLIGHT_OPACITY 
            start_node = edge['source']
            end_node = edge['target']
            if start_node in path_nodes_set and end_node in path_nodes_set:
                format_edge = self._formatPathEdge(start_node, end_node) 
                if format_edge in path_edges2path_ids:
                    #path ids are rewritten as 1, 2 ,4, 8, 16. so the sum will not be repeated
                    edge['color'] = sum(path_edges2path_ids[format_edge])
                    edge['length'] = 400 + random.random()*100
                    edge['opacity'] = 1.0
            elif start_node in path_nodes_set:
                around_path_nodes_set.add(end_node)
            elif end_node in path_nodes_set:
                around_path_nodes_set.add(start_node)

        #add nodes on the path
        for node_id in path_nodes_set:
            node = {'id': node_id, 'size': config.NODE_DEFAULT_SIZE, 'color': 0, 'highlight': 1, 'opacity': 1.0}
            self.graph_nodes.append(node) 
                
        #add nodes around the path
        for node_id in around_path_nodes_set:
            node = {'id': node_id, 'size': config.NODE_DEFAULT_SIZE, 'color': 0, 'highlight': 0, 'opacity': config.UNHIGHLIGHT_OPACITY}
            self.graph_nodes.append(node) 

    def _generateGraphEdges(self, matGraphFile): 
        self.graph_edges = []
        graph_edges_dict = dict()

        with open(matGraphFile) as f:
            for line in f:
                edge_nodes = line.strip().split()
                format_edge = self._formatPathEdge(str(edge_nodes[0].strip()), str(edge_nodes[1].strip()))
                if format_edge not in graph_edges_dict:
                    graph_edges_dict[format_edge] = 0
                graph_edges_dict[format_edge] += 1

        edge_weights = graph_edges_dict.values()
        edge_max_weight = max(edge_weights) + 1.0 
        edge_min_weight = min(edge_weights) 
        for format_edge, weight in graph_edges_dict.iteritems():
            width = 1.0 + ((weight- edge_min_weight) * (config.NODE_DEFAULT_SIZE - 1.0) / (edge_max_weight- edge_min_weight))
            edge = {'source': format_edge[0], 'target': format_edge[1],
                    'length': 100 + random.random() * 50, 'width': width, 'color': 0, 'opacity': 1.0}
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
        matGraphFile = helper.getGraph(self.graph_name)
        self._generateGraphEdges(matGraphFile)

        #read graph nodes 
        if self.graph_operator == 'rank':
            #read query result
            query_result = queryConsole.readTable(self.graph_op_result_name, self.graph_condition)
            keep_nodes = self._generateRankSelectNodes(query_result.row_content)

            #read graph structure(cluster nodes)
            origin_result = queryConsole.readTable('crea_clu_' + self.graph_name, "")
            self._generateClusterGraphNodes(origin_result.row_content, keep_nodes)

        elif self.graph_operator == 'path':
            query_result = queryConsole.readTable(self.graph_op_result_name, self.graph_condition)
            self._generatePathGraphNodes(query_result.row_content)

        else:
            query_result = queryConsole.readTable(self.graph_op_result_name, "")

            if self.graph_operator == 'cluster':
                self._generateClusterGraphNodes(query_result.row_content, {})
            else:
                self._generateClusterGraphNodes(query_result.row_content, {})

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
        if result_type not in ['string', 'table', 'graph', 'table_graph']:
            raise TypeError('Query result type must be string, table , graph or table_graph') 
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
