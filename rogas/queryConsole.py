'''
The queryConsole is to read the query input, show query results and display error information

@author: minjian
'''
import psycopg2
import queryParser
import matGraphProcessor
import clusterExecutor as cExe
import time
import os
from resultManager import QueryResult, GraphResult, TableResult, TableGraphResult, SingleResultManager
import config

#this array is used to store the name of materialized graphs;
mat_graph_cache = []

#this array is used to store each function and its related result table name
graphQueryAndResult = dict()

#starts to execute the input query
def execQuery(conn, cur, executeCommand):
    queryResult = QueryResult()
    lowerCaseCommand = executeCommand.lower()
    
    #graph query contains rank, cluster and path operation
    if ("rank(" in lowerCaseCommand) or ("cluster(" in lowerCaseCommand)or ("path(" in lowerCaseCommand):
        startTime = time.time()
        
        newExecuteCommand, graphOperationInfo = queryParser.queryAnalyse(executeCommand, conn, cur, mat_graph_cache, graphQueryAndResult)
        #newExecuteCommand = graphProcessor.queryAnalyse(executeCommand, conn, cur)
        #print "Total operation time is: ", (time.time() - startTime)
        #print newExecuteCommand  #for debug
        cur.execute(newExecuteCommand[:]) #remove the first space

        queryResult.setType("table_graph")
        tableResult = SingleResultManager.extractTableResultFromCursor(cur)
        graphResult = GraphResult(graphOperationInfo[0], graphOperationInfo[1], graphOperationInfo[2], graphOperationInfo[3], graphOperationInfo[4]) 
        graphResult.generateGraph()
        queryResult.setContent(TableGraphResult(tableResult, graphResult))
    
    #query about creating or dropping a materialised graph    
    elif ("create" in lowerCaseCommand[:7] or "drop" in lowerCaseCommand[:5]) and ("ungraph" in lowerCaseCommand or "digraph" in lowerCaseCommand):
        newExecuteCommand, graphName, graphType = matGraphProcessor.processCommand(executeCommand, conn, cur)
        eIndex = newExecuteCommand.index("view")
        cur.execute(newExecuteCommand[:]) #remove the first space
        #print newExecuteCommand[:eIndex] + "graph"

        if "drop" in lowerCaseCommand:
            queryResult.setType("string")
            queryResult.setContent("Drop Graph Done")
        else:
            tableResult = readTable(graphName, "")
            #write graph to file
            tmpGraphDir = "/dev/shm/RG_Tmp_Graph/"
            createGraphName = 'crea_clu_' + graphName
            with open(tmpGraphDir + createGraphName, 'w') as f:
                for edge in tableResult.row_content:
                    f.write(str(edge[0]) + '\t' + str(edge[1]) + os.linesep)

            #keep cluster result in database
            clusterCommands = [createGraphName, 'MC', graphType, [], '', createGraphName]
            cExe.processCommand(clusterCommands, conn, cur, False)

            queryResult.setType('graph')
            graphResult = GraphResult('all', graphType, createGraphName, createGraphName,'') 
            graphResult.generateGraph()
            queryResult.setContent(graphResult)
    
    elif ("refresh" in lowerCaseCommand[:8]):
        if  ("ungraph" in lowerCaseCommand) or  ("digraph" in lowerCaseCommand):
            mat_graphName = (lowerCaseCommand.split()[-1])[:-1]
            if mat_graphName in mat_graph_cache:
                mat_graph_cache.remove(mat_graphName)
            g_index = lowerCaseCommand.index("graph");
            executeCommand = executeCommand[:].replace(executeCommand[g_index - 2 : g_index + 5], "materialized view")
            cur.execute(executeCommand)
            queryResult.setType("string")
            queryResult.setContent("Graph Refreshed")
            
            try:
                cur.execute("select tablename from pg_tables where schemaname like 'pg_temp%';")
                temp_tables = cur.fetchall()
                graphQueryAndResult.clear()
                for each in temp_tables:
                    for each_table in each:
                        cur.execute("drop table %s;" %each_table)
            except Exception as reason:
                conn.commit()
                cur.close()
            

            
    #normal relational query without any graph functions
    else:
        #print executeCommand[:]
        cur.execute(executeCommand[:])  #remove the first space
        queryResult.setType("table")
        queryResult.setContent(SingleResultManager.extractTableResultFromCursor(cur))

    conn.commit() 
    return queryResult

SingleConnection = psycopg2.connect(database=config.DB, user=config.DB_USER, password=config.DB_PASSWORD, port=config.DB_PORT)

def prepare():
    homeDir = os.environ['HOME']
    memDir = "/dev/shm"
    
    if os.path.exists(homeDir + "/RG_Mat_Graph") == False:
        os.mkdir(homeDir + "/RG_Mat_Graph")
        
    if os.path.exists(memDir + "/RG_Tmp_Graph") == False:
        os.mkdir(memDir + "/RG_Tmp_Graph")
        
    try:
        pre_cur = SingleConnection.cursor()
        pre_cur.execute("select matgraphname from my_matgraphs;" )
        mat_graph_result = pre_cur.fetchall()
        for each_graph in mat_graph_result:
            for each in each_graph:
                pre_cur.execute("refresh materialized view  %s;" %each)
    except Exception as reason:
        pre_cur.close()

def start(query):
    cur = SingleConnection.cursor()
    
    start_time = time.time()
    queryResult = QueryResult()
    try:
        queryResult = execQuery(SingleConnection, cur, query)
        #print "Total query time is: ", (time.time() - start_time)
        os.system("rm -fr /dev/shm/RG_Tmp_Graph/*")  #clear graphs on-the-fly
    except Exception as reason:
        queryResult.setType("string")
        queryResult.setContent(str(reason))

    needKeepCursor = False
    if queryResult.result_type == "table":
        needKeepCursor = (queryResult.result_content.is_end == 0)
    elif queryResult.result_type == "table_graph":
        needKeepCursor = (queryResult.result_content.table_result.is_end == 0)
    if needKeepCursor == False:
        cur.close()

    SingleConnection.rollback()

    return queryResult

def fetch(query_id, is_next):
    queryResult = QueryResult()

    queryResult.setType("table")
    queryResult.setContent(SingleResultManager.extractTableResultById(query_id, is_next))

    return queryResult

def readTable(table_name, condition):
    cur = SingleConnection.cursor()
    cur.execute('select * from ' + table_name + ' ' + condition + ';') 
    tableResult = SingleResultManager.extractTableResultFromCursor(cur, is_all=True)
    cur.close()

    SingleConnection.commit() 
    SingleConnection.rollback()
    return tableResult
