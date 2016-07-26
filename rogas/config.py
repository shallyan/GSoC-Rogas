'''
This is the configuration

@author Yan Xiao
'''

#information to connect to database
DB = "acm"
DB_USER = "postgres"
DB_PASSWORD = "111"
DB_PORT = 5432

#each page has 10 records
PAGE_MAX_NUM = 10 

#graph max nodes
#max top K rank nodes
RANK_NODE_MAX_NUM = 20

GRAPH_NODE_MAX_NUM = 400

#max paths num, because of max 20 colors
PATH_MAX_NUM = 20

#visualization
NODE_MIN_SIZE = 15
NODE_MAX_SIZE = 30 
NODE_DEFAULT_SIZE = 10

UNHIGHLIGHT_OPACITY = 0.2

#whether graph_tool support openmp
IS_GRAPH_TOOL_OPENMP = True 
