#![Logo](https://cecs.anu.edu.au/sites/default/files/styles/anu_doublenarrow_440_scale/public/images/rogas-web.jpg?itok=JfEfhc1_)
Rogas(https://github.com/CornucopiaRG/Rogas) is a project for Network Analytics

## Introduction
Rogas not only can provides a high-level declarative query language to 
formulate analysis queries, but also can unify different graph algorithms 
within the relational environment for query processing.
<br>
<br>
The Rogas has three main components: (1) a hybrid data model, which 
integrates graphs with relations so that we have these two types of data 
structures respectively for network analysis and relational analysis; 
(2) a SQL-like query language, which extends standard SQL with 
graph constructing, ranking, clustering, and path finding operations; 
(3) a query engine, which is built upon PostgreSQL and can efficiently process 
network analysis queries using various graph systems and 
their supporting algorithms.
<br>
<br>

## Work Description during Google Summer of Code 2016
My work is contained in this repository, not including the file in Rogas which is not authored with Yan Xiao. Specifically, with my mentors Minjian Liu and Qing Wang's guidance, it contains three parts:

- Design and implement the Web GUI
- Design and implement the visualisation of graph operations(CREATE, RANK, PATH, CLUSTER) 
- Design and implement the backend server and modify Rogas for connecting to front-end

## Algorithms for Large Graph Visualization
### Graph Cluster Operation 
- 1) Rescale the size of each cluster according to their proportion
- 2) Score each node according to their inner-cluster edges, cluster-cluster edges and target node's degree
- 3) Find max connected component in each cluster
- 4) Get specified number nodes in max connected component from high score to low score
- 5) Find neighbor nodes around the picked nodes

### Graph Rank Operation 
- 1) Get ranked nodes
- 2) Find nodes on the shortest path between ranked nodes
- 3) Find nodes around the ranked nodes

### Graph Path Operation 
- 1) Get nodes on the path
- 2) Find nodes around the path

## Main Features
- List information about entities and relationships of the relational core and materialised graphs
- Database info panel can be customised by users
- Query input panel can be extended to a larger space for complicated queries
- Query and its results as browser tabs
- Asynchronous execution with loading animation
- Support paged loading for large tables 
- Support graph creation, rank, path, cluster visualization
- Support large graph visualization
- Support drag, doubleclick, zoom in/out operations and so on 
- Support relation - graph data mapping
- Support dynamic setting

## Work Screenshots
- Graph CREATION Operation
![create](http://ww1.sinaimg.cn/large/005WEw7ygw1f6ui3u7iy9j31kw0zkqgk.jpg)

- Graph RANK Operation: Realtion Tab
![rankrelation](http://ww1.sinaimg.cn/large/005WEw7ygw1f6ui8fa8eej31kw0zkafp.jpg)

- Graph RANK Operation: Graph Visualization
![rankgraph](http://ww4.sinaimg.cn/large/005WEw7yjw1f6uiak0rjuj31kw0zkwrz.jpg)

- Graph PATH Operation: Graph Visualization
![path](http://ww3.sinaimg.cn/large/005WEw7yjw1f6uib6bntxj31kw0zkn4y.jpg)

- Graph CLUSTER Operation: Graph Visualization
![cluster](http://ww3.sinaimg.cn/large/005WEw7yjw1f6uig5hos1j31kw0zk12k.jpg)

- Relation - Graph Data Mapping
![map](http://ww4.sinaimg.cn/large/005WEw7yjw1f6uigv6b59j31kw0zkdna.jpg)

- Database Info
![dbinfo](http://ww3.sinaimg.cn/large/005WEw7ygw1f6uiicglh4j31kw0zkagj.jpg)

## Dependencies 
* Python 2.7
* Tornado: http://www.tornadoweb.org/en/stable/
* Postgresql: https://www.postgresql.org/ 
* Psycopg: http://initd.org/psycopg/
* Graph-tool: http://graph-tool.skewed.de/
* SNAP: http://snap.stanford.edu/snappy/index.html
* NetworkX: http://networkx.github.io/  

Note: If you use Mac OS, the Graph-tool installed doesn't support OpenMP by default, so that you need set IS\_GRAPH\_TOOL\_OPENMP = False in rogas/config.py.
<br>
<br>
We also make use of Bootstrap(http://getbootstrap.com/), D3.js(https://d3js.org) and ExpandingTextareas(https://github.com/bgrins/ExpandingTextareas), which are integrated into the system so that you don't need install them by yourself.

## How to Run
- Set up your database information in rogas.config.py to connect to Postgresql
- Python run.py

## More Information
More details about the Rogas, please refer to 
the thesis "Towards a Unified Framework for Network Analytics" collected in 
Australian National University (http://users.cecs.anu.edu.au/~u5170295/publications/thesis-minjian.pdf). You can also 
contact *minjian.liu@anu.edu.au* or *qing.wang@anu.edu.au* for more information.
