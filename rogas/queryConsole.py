'''
The queryConsole is to read the query input, show query results and display error information

@author: minjian
'''
import psycopg2
import queryParser
import matGraphProcessor
import time
import os

class TableResult(object):
    def __init__(self, column_list=None, row_content=None):
        self.setColumnList(column_list)
        self.setRowContent(row_content)

    def setColumnList(self, column_list):
        self.column_list = column_list

    def setRowContent(self, row_content):
        self.row_content = row_content 

    def asDict(self):
        return {'column_list': self.column_list, 'row_content': self.row_content}

class QueryResult(object):
    def __init__(self, result_type="string", result_content="None"):
        #type: string, table
        self.setType(result_type)
        self.setContent(result_content)

    def setType(self, result_type):
        if result_type not in ["string", "table"]:
            raise TypeError("Query result type must be string or table") 
        self.result_type = result_type
    
    def setContent(self, result_content):
        self.result_content = result_content
    
    def asDict(self):
        content_val = self.result_content.asDict() if self.result_type == "table" else self.result_content
        return {'type': self.result_type, 'content': content_val}

#starts to execute the input query
def execQuery(conn, cur, executeCommand):
    queryResult = QueryResult()
    lowerCaseCommand = executeCommand.lower()
    
    #graph query contains rank, cluster and path operation
    if ("rank" in lowerCaseCommand) or ("cluster" in lowerCaseCommand)or ("path" in lowerCaseCommand):
        startTime = time.time()
        
        newExecuteCommand = queryParser.queryAnalyse(executeCommand, conn, cur)
        #newExecuteCommand = graphProcessor.queryAnalyse(executeCommand, conn, cur)
        #print "Total operation time is: ", (time.time() - startTime)
        #print newExecuteCommand  #for debug
        cur.execute(newExecuteCommand[:]) #remove the first space
        queryResult.setType("table")
        queryResult.setContent(ExtractTableResult(conn, cur))
    
    #query about creating or dropping a materialised graph    
    elif ("create" in lowerCaseCommand or "drop" in lowerCaseCommand) and ("ungraph" in lowerCaseCommand or "digraph" in lowerCaseCommand):
        newExecuteCommand = matGraphProcessor.processCommand(executeCommand, conn, cur)
        eIndex = newExecuteCommand.index("view")
        cur.execute(newExecuteCommand[:]) #remove the first space
        conn.commit()
        #print newExecuteCommand[:eIndex] + "graph"
        queryResult.setType("string")
        queryResult.setContent("Graph Operation Done")
    
    #normal relational query without any graph functions
    else:
        #print executeCommand[:]
        cur.execute(executeCommand[:])  #remove the first space
        queryResult.setType("table")
        queryResult.setContent(ExtractTableResult(conn, cur))

    return queryResult

#extract results received from the database
def ExtractTableResult(conn, cur):
    column_list = [desc[0] for desc in cur.description]
    rows_content = []

    rows = cur.fetchall()
    for each_row in rows:
        one_row_content = [each_col for each_col in each_row]
        rows_content.append(one_row_content)
    conn.commit() 

    return TableResult(column_list, rows_content)
     
def start(query):
    #starts the main function   
    homeDir = os.environ['HOME']
    memDir = "/dev/shm"
    
    if os.path.exists(homeDir + "/RG_Mat_Graph") == False:
        os.mkdir(homeDir + "/RG_Mat_Graph")
        
    if os.path.exists(memDir + "/RG_Tmp_Graph") == False:
        os.mkdir(memDir + "/RG_Tmp_Graph")    
           
    #Here is connect to your PostgreSQL
    #Change you database, user and port here
    #db = "acm_small"
    db = "stackoverflow"
    dbUser = "postgres"
    dbPwd = "111"
    dbPort = 5432
    
    conn = psycopg2.connect(database=db, user=dbUser, password=dbPwd, port=dbPort)
    cur = conn.cursor()
    
    start_time = time.time()
    queryResult = QueryResult()
    try:
        queryResult = execQuery(conn, cur, query)
        #print "Total query time is: ", (time.time() - start_time)
        os.system("rm -fr /dev/shm/RG_Tmp_Graph/*")  #clear graphs on-the-fly
        queryParser.graphQueryAndResult.clear()  #clear parser's dictionary for result table names and graph sub-queries
    except psycopg2.ProgrammingError as reason:
        queryResult.setType("string")
        queryResult.setContent(str(reason))
    finally:
        cur.close()
        conn.close()

    return queryResult
