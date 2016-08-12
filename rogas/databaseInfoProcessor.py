'''
The databaseInfoProcessor is to manage the database info, including realtion core and graphical view

@author: Yan Xiao
'''

import config
import StringIO 
from resultManager import QueryResult, TableResult
import helper

#two cases: relation core entire info and relation table info
def dealWithRelationCoreMetaInfo(cmd, isCore=True):
    infoString = helper.subprocessCmd(cmd)

    inputStream = StringIO.StringIO(infoString)
    relationCoreLines = inputStream.readlines()
    
    queryResult = QueryResult()
    if len(relationCoreLines) < 2:
        queryResult.setType("string")
        queryResult.setContent("Empty relation core information")
    else:
        queryResult.setType("table")
        #table header
        tableHeader = relationCoreLines[1]
        tableHeaderLst = [str(col).strip() for col in tableHeader.split('|')]
        #table content
        rowsContent = []
        endIndex = len(relationCoreLines)-2 if isCore else len(relationCoreLines)-1
        for index in xrange(3, endIndex):
            if relationCoreLines[index].strip() == "Indexes:":
                break
            oneRowContent = [str(col).strip() for col in relationCoreLines[index].split('|')]
            rowsContent.append(oneRowContent)

        queryResult.setContent(TableResult(tableHeaderLst, rowsContent))

    return queryResult

def getRelationCoreInfo():
    cmd = "psql -d " + config.DB + " -c '\d'"
    return dealWithRelationCoreMetaInfo(cmd, True)

def getRelationTableInfo(table_name):
    cmd = "psql -d " + config.DB + " -c '\d " + table_name + "'"
    return dealWithRelationCoreMetaInfo(cmd, False)

def getGraphicalViewInfo():
    from queryConsole import readTable
    queryResult = QueryResult()

    tableResult = readTable("my_matgraphs", "");
    if tableResult.total_num == 0:
        queryResult.setType("string")
        queryResult.setContent("Empty graphical view information")
    else:
        queryResult.setType("table")
        queryResult.setContent(tableResult)

    return queryResult
