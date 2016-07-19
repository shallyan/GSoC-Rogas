
'''
This file contains some useful functions

@author: Yan Xiao 
'''

import os

#get the graph from materialised graph dir or tmp graph dir
def getGraph(graphName):
    matGraphDir = os.environ['HOME'] + "/RG_Mat_Graph/"
    tmpGraphDir = "/dev/shm/RG_Tmp_Graph/"
    
    if os.path.exists(tmpGraphDir + graphName):
        return tmpGraphDir + graphName
    elif os.path.exists(matGraphDir + graphName):
        return matGraphDir + graphName
    else:
        raise RuntimeError, "No such graph!!"

