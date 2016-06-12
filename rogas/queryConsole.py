'''
The queryConsole is to read the query input, show query results and display error information

@author: minjian
'''

import psycopg2
import queryParser
import matGraphProcessor
import time
import os
from Tkinter import * #GUI package
from pylsy import pylsytable #for print table

class QueryResult(object):
    def __init__(self):
        #type: string, table
        self.result_type = "string" 
        self.result_content = "None"

    def setType(self, result_type):
        if result_type not in ["string", "table"]:
            raise TypeError("Query result type must be string or table") 
        self.result_type = result_type
    
    def setContent(self, result_content):
        self.result_content = result_content

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
    colnames = [desc[0] for desc in cur.description]
    table = pylsytable(colnames)
    rows = cur.fetchall()
    for each_row in rows:
        for col_index, each_col in enumerate(each_row):
            table.append_data(colnames[col_index], str(each_col))
    conn.commit() 
    return table
     
def start(query):
    print 'Query:', query
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
    try:
        queryResult = execQuery(conn, cur, query)
        print queryResult.result_content
        #print "Total query time is: ", (time.time() - start_time)
        os.system("rm -fr /dev/shm/RG_Tmp_Graph/*")  #clear graphs on-the-fly
        queryParser.graphQueryAndResult.clear()  #clear parser's dictionary for result table names and graph sub-queries
    except psycopg2.ProgrammingError as reason:
        print str(reason)
    finally:
        cur.close()
        conn.close()

query = 'select * from labelled_by limit 3;'
start(query)
