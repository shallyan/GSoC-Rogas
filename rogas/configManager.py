'''
This is the configuration manager

@author Yan Xiao
'''

import os
import json

config_dump_file = 'config.dump'

class ConfigManager(object):
    def __init__(self):
        self.load()

    def _reInit(self, graph_node_max_num=400, rank_node_max_num=20, path_max_num=20, node_min_size=15, node_max_size=30, node_default_size=10, edge_min_width=2, edge_max_width=10, unhighlight_opacity=0.2):
        self.GRAPH_NODE_MAX_NUM = graph_node_max_num
        self.RANK_NODE_MAX_NUM = rank_node_max_num
        self.PATH_MAX_NUM = path_max_num
        self.NODE_MIN_SIZE = node_min_size
        self.NODE_MAX_SIZE = node_max_size
        self.NODE_DEFAULT_SIZE = node_default_size
        self.EDGE_MIN_WIDTH = edge_min_width
        self.EDGE_MAX_WIDTH = edge_max_width
        self.UNHIGHLIGHT_OPACITY = unhighlight_opacity
    
    def reInitWithDict(self, config_dict, is_dump=True):
        self._reInit()

        if is_dump:
            with open(config_dump_file, 'w') as f:
                json.dump(config_dict, f)

        for key, value in config_dict.iteritems():
            setattr(self, key, value)
            
    
    def load(self):
        #default init because config file may not contain each item
        self._reInit()

        if os.path.exists(config_dump_file):
            with open(config_dump_file) as f:
                config_dict = json.load(f)
                self.reInitWithDict(config_dict, False)

SingleConfigManager = ConfigManager()
